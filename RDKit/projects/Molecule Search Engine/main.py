import os
import json
import urllib.request
import urllib.parse
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from rdkit import Chem, DataStructs
from rdkit.Chem import rdFingerprintGenerator
import pandas as pd

app = FastAPI()

# Add CORS Middleware to allow frontend to fetch data
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

generator = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)

# Load or Generate the Pickle file
dataset_csv = r"c:\Users\rasel\jvai projects\Agents\AI-Engineer-for-Life-Sciences-Libraries\Cheminformatics\RDKit\dataset\molecules_100.csv"
pkl_path = "molecules.pkl"

if os.path.exists(pkl_path):
    df = pd.read_pickle(pkl_path)
else:
    print("Pickle file not found. Generating from CSV...")
    df = pd.read_csv(dataset_csv)
    df['Mol'] = df['SMILES'].apply(Chem.MolFromSmiles)
    df = df.dropna(subset=['Mol'])
    df['Fingerprint'] = df['Mol'].apply(generator.GetFingerprint)
    df.to_pickle(pkl_path)
    print("Pickle file generated successfully.")

@app.get("/search")
def search_molecule(query: str, top: int = 10):
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
        
    # convert query SMILES
    query_mol = Chem.MolFromSmiles(query)
    resolved_smiles = query
    
    if query_mol is None:
        # Try resolving the query as a molecule name via PubChem API
        try:
            pubchem_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{urllib.parse.quote(query)}/property/CanonicalSMILES/JSON"
            with urllib.request.urlopen(pubchem_url) as response:
                data = json.loads(response.read().decode())
                props = data['PropertyTable']['Properties'][0]
                for k, v in props.items():
                    if 'SMILES' in k:
                        resolved_smiles = v
                        break
                if resolved_smiles:
                    query_mol = Chem.MolFromSmiles(resolved_smiles)
        except Exception as e:
            print(f"PubChem API Error: {e}")

    if query_mol is None:
        raise HTTPException(status_code=400, detail=f"Could not parse '{query}' as SMILES or find it as a molecule name.")

    query_fp = generator.GetFingerprint(query_mol)

    df["similarity"] = df["Fingerprint"].apply(
        lambda fp: DataStructs.TanimotoSimilarity(query_fp, fp)
    )

    result = df.sort_values("similarity", ascending=False).head(top)

    # Rename 'Name' to 'name' to match frontend expectations
    return result[["Name", "SMILES", "similarity"]].rename(columns={"Name": "name"}).to_dict(orient="records")