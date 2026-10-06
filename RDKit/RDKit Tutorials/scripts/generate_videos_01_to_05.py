#!/usr/bin/env python3
"""
Generator script for Video Tutorials 01 to 05 of the RDKit Master Playlist.
Each notebook is structured for a 25-30 minute comprehensive video lesson.
"""

import os
import nbformat as nbf

def create_nb(cells):
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3 (ipykernel)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.12.0"
        }
    }
    for cell_type, content in cells:
        if cell_type == "markdown":
            nb.cells.append(nbf.v4.new_markdown_cell(content))
        elif cell_type == "code":
            nb.cells.append(nbf.v4.new_code_cell(content))
    return nb

# ==============================================================================
# VIDEO 01: RDKit Fundamentals & Molecular Representations
# ==============================================================================
def build_video_01():
    cells = [
        ("markdown", """# 🎥 Video 01: RDKit Fundamentals & Molecular Representations
**RDKit Masterclass — From Zero to Drug Discovery AI**
* **Duration:** ~25 - 30 Minutes
* **Curriculum Level:** LEVEL 1 — RDKit Fundamentals (Topics 01, 02, 03, 04)
* **Target Audience:** Cheminformatics Engineers, AI for Drug Discovery Researchers, Computational Chemists

---

### ⏱️ Video Agenda & Timestamps
* **00:00 - 04:30** | Introduction: What is RDKit? Cheminformatics vs Bioinformatics
* **04:30 - 09:00** | RDKit Architecture & The Core `Mol` Object (Atoms, Bonds, Rings)
* **09:00 - 14:00** | Molecular Representations: SMILES, SMARTS, MolBlock, InChI & InChIKey
* **14:00 - 19:30** | Converting SMILES to Mol: Validation, Implicit Hydrogens & Sanitization
* **19:30 - 24:00** | Converting Mol to SMILES: Canonicalization, Kekulization & Aromaticity Models
* **24:00 - 28:00** | Live Coding Exercise: Analyzing Blockbuster Drug Molecules
* **28:00 - 30:00** | Summary, Common Pitfalls & Next Episode Teaser

---

### 🎯 Learning Objectives
1. Understand RDKit's C++ core with Python bindings architecture.
2. Distinguish between 1D (SMILES/InChI), 2D (MolBlock/SDF), and 3D molecular representations.
3. Master `Chem.MolFromSmiles()` and handle invalid SMILES gracefully without script crashes.
4. Understand canonical SMILES, isomeric SMILES, and the difference between Kekule and aromatic forms.
5. Inspect individual atoms and bonds programmatically."""),

        ("code", """# Step 0: Environment Verification and Imports
import rdkit
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import IPythonConsole
import pandas as pd

# Configure high-resolution inline rendering for Jupyter
IPythonConsole.ipython_useSVG = True
IPythonConsole.molSize = (350, 250)

print(f"✅ RDKit Version: {rdkit.__version__}")
print("Environment initialized successfully!")"""),

        ("markdown", """## 1. What is RDKit & What is a `Mol` Object?
In bioinformatics, we represent biological macromolecules (DNA, RNA, proteins) primarily as **linear 1D sequences** of characters ($A, C, G, T$ or 20 amino acid letters).
In **cheminformatics**, small drug molecules are **2D/3D chemical graphs**:
* **Nodes:** Atoms (Carbon, Nitrogen, Oxygen, Halogens, etc.) with specific oxidation states, formal charges, and stereochemistry.
* **Edges:** Chemical bonds (single, double, triple, aromatic) with geometric configurations (cis/trans, stereochemical wedges).

In RDKit, every molecule is represented as an instance of `rdkit.Chem.rdchem.Mol`."""),

        ("code", """# Create our first molecule: Aspirin (Acetylsalicylic acid)
aspirin_smiles = "CC(=O)Oc1ccccc1C(=O)O"
mol_aspirin = Chem.MolFromSmiles(aspirin_smiles)

print(f"Object type: {type(mol_aspirin)}")
print(f"Number of heavy atoms: {mol_aspirin.GetNumAtoms()}")
print(f"Number of bonds: {mol_aspirin.GetNumBonds()}")

# Display the 2D depiction inline
mol_aspirin"""),

        ("markdown", """## 2. Inspecting Atoms, Bonds, and Rings
Let's explore the graph structure of our molecule. We can iterate over all atoms and bonds to extract fundamental chemical properties."""),

        ("code", """# Inspecting atoms
atom_data = []
for atom in mol_aspirin.GetAtoms():
    atom_data.append({
        "Index": atom.GetIdx(),
        "Symbol": atom.GetSymbol(),
        "AtomicNum": atom.GetAtomicNum(),
        "FormalCharge": atom.GetFormalCharge(),
        "Hybridization": str(atom.GetHybridization()),
        "IsAromatic": atom.GetIsAromatic(),
        "TotalNumHs": atom.GetTotalNumHs(),
        "InRing": atom.IsInRing()
    })

df_atoms = pd.DataFrame(atom_data)
df_atoms.head(10)"""),

        ("code", """# Inspecting chemical bonds
bond_data = []
for bond in mol_aspirin.GetBonds():
    bond_data.append({
        "BondIdx": bond.GetIdx(),
        "BeginAtom": f"{bond.GetBeginAtom().GetSymbol()}_{bond.GetBeginAtomIdx()}",
        "EndAtom": f"{bond.GetEndAtom().GetSymbol()}_{bond.GetEndAtomIdx()}",
        "BondType": str(bond.GetBondType()),
        "IsAromatic": bond.GetIsAromatic(),
        "IsConjugated": bond.GetIsConjugated()
    })

df_bonds = pd.DataFrame(bond_data)
df_bonds.head(10)"""),

        ("markdown", """## 3. SMILES, InChI, and InChIKey
Different notations exist to represent chemical structures:
1. **SMILES (Simplified Molecular Input Line Entry System):** Human-readable, compact, graph-traversal string.
2. **InChI (International Chemical Identifier):** Layered IUPAC standard string describing formula, connectivity, hydrogens, charge, and stereochemistry.
3. **InChIKey:** Fixed-length 27-character SHA-256 hash of the InChI string, ideal for database indexing, search engines, and web queries."""),

        ("code", """# Generate canonical SMILES, InChI, and InChIKey
canonical_smiles = Chem.MolToSmiles(mol_aspirin)
inchi = Chem.MolToInchi(mol_aspirin)
inchikey = Chem.MolToInchiKey(mol_aspirin)

print(f"Canonical SMILES: {canonical_smiles}")
print(f"InChI:            {inchi}")
print(f"InChIKey:         {inchikey}")"""),

        ("markdown", """## 4. Handling Invalid SMILES & Error Recovery
In real-world data science, datasets contain typos, broken SMILES, or chemically impossible valences (e.g. 5-valent carbon).
By default, `Chem.MolFromSmiles()` prints an error to stderr and returns `None`. Your code must handle `None` gracefully!"""),

        ("code", """# Testing valid and invalid SMILES
test_smiles = [
    ("Aspirin", "CC(=O)Oc1ccccc1C(=O)O"),
    ("Ibuprofen", "CC(C)Cc1ccc(cc1)C(C)C(=O)O"),
    ("Invalid Valence Carbon", "C(=O)(=O)(=O)C"), # Impossible pentavalent/hexavalent carbon
    ("Broken Syntax", "c1ccccc"),                 # Unclosed ring
    ("Paracetamol", "CC(=O)Nc1ccc(O)cc1")
]

parsed_molecules = {}
for name, smi in test_smiles:
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        print(f"❌ Failed to parse '{name}': invalid SMILES -> {smi}")
        parsed_molecules[name] = None
    else:
        print(f"✅ Successfully parsed '{name}': {mol.GetNumAtoms()} heavy atoms")
        parsed_molecules[name] = mol"""),

        ("markdown", """## 5. Canonicalization, Kekulization & Aromaticity
A single chemical compound can be written in many non-canonical SMILES forms.
For example, ethanol can be `CCO`, `OCC`, or `C(O)C`.
RDKit canonicalizes all variations to a single unique string!

Furthermore, aromatic systems can be represented in **aromatic form** (`c1ccccc1`) or **Kekule form** with alternating single and double bonds (`C1=CC=CC=C1`)."""),

        ("code", """# Multiple SMILES representing the same compound
smi_variants = ["CCO", "OCC", "C(O)C"]
for s in smi_variants:
    m = Chem.MolFromSmiles(s)
    print(f"Input: {s:<8} -> Canonical: {Chem.MolToSmiles(m)}")

# Kekulization vs Aromatic SMILES
benzene = Chem.MolFromSmiles("c1ccccc1")
print(f"Standard Aromatic SMILES: {Chem.MolToSmiles(benzene)}")

# Kekulize the molecule (assign explicit alternating single and double bonds)
Chem.Kekulize(benzene)
print(f"Kekule SMILES:           {Chem.MolToSmiles(benzene, kekuleSmiles=True)}")"""),

        ("markdown", """## 6. Isomeric SMILES & Stereochemistry
Stereochemistry is vital in pharmacology: one enantiomer may be an active life-saving drug, while the opposite enantiomer could be inactive or toxic (e.g., Thalidomide).
RDKit preserves stereochemistry using `@` and `@@` for tetrahedral chiral centers, and `/` or `\\` for cis/trans double bonds."""),

        ("code", """# L-Alanine vs D-Alanine
l_alanine = Chem.MolFromSmiles("N[C@@H](C)C(=O)O")
d_alanine = Chem.MolFromSmiles("N[C@H](C)C(=O)O")

print(f"L-Alanine Isomeric SMILES: {Chem.MolToSmiles(l_alanine, isomericSmiles=True)}")
print(f"L-Alanine Non-isomeric:    {Chem.MolToSmiles(l_alanine, isomericSmiles=False)}")
print(f"D-Alanine Isomeric SMILES: {Chem.MolToSmiles(d_alanine, isomericSmiles=True)}")

Draw.MolsToGridImage([l_alanine, d_alanine], legends=["L-Alanine (@ chiral)", "D-Alanine (@@ chiral)"])"""),

        ("markdown", """## 7. 🎯 Video Hands-On Challenge & Solution
### Problem:
Given a list of 5 blockbuster drugs:
1. Parse each into an RDKit Mol object.
2. Extract the canonical SMILES, molecular formula, number of rings, and heavy atom count.
3. Handle any potential parsing failures safely.
4. Render them in a clean 2D comparison grid!"""),

        ("code", """from rdkit.Chem import rdMolDescriptors

drugs = {
    "Caffeine": "Cn1cnc2c1c(=O)n(c(=O)n2C)C",
    "Imatinib (Gleevec)": "Cc1ccc(cc1Nc2nccc(n2)c3cccnc3)NC(=O)c4ccc(cc4)CN5CCN(CC5)C",
    "Atorvastatin (Lipitor)": "CC(C)c1c(C(=O)Nc2ccccc2)c(c3ccc(F)cc3)c(c4ccccc4)n1CCC(O)CC(O)CC(=O)O",
    "Penicillin V": "CC1(C(N2C(S1)C(C2=O)NC(=O)COc3ccccc3)C(=O)O)C",
    "Gefitinib (Iressa)": "COc1cc2ncnc(Nc3ccc(F)c(Cl)c3)c2cc1OCCCN4CCOCC4"
}

results = []
valid_mols = []
legends = []

for name, smi in drugs.items():
    mol = Chem.MolFromSmiles(smi)
    if mol:
        formula = rdMolDescriptors.CalcMolFormula(mol)
        num_rings = rdMolDescriptors.CalcNumRings(mol)
        canon_smi = Chem.MolToSmiles(mol)
        
        results.append({
            "Drug": name,
            "Formula": formula,
            "HeavyAtoms": mol.GetNumAtoms(),
            "Rings": num_rings,
            "Canonical_SMILES": canon_smi
        })
        valid_mols.append(mol)
        legends.append(f"{name}\\n{formula}")

df_results = pd.DataFrame(results)
print("=== BLOCKBUSTER DRUGS SUMMARY TABLE ===")
display(df_results[["Drug", "Formula", "HeavyAtoms", "Rings"]])

# Display 2D grid image
Draw.MolsToGridImage(valid_mols, legends=legends, molsPerRow=3, subImgSize=(300, 200))"""),

        ("markdown", """## 8. Summary & Key Takeaways
* **`Mol` Graph Object:** RDKit represents molecules as rich chemical graphs where atoms are nodes and bonds are edges.
* **SMILES Parsing:** Always check `if mol is None:` when loading SMILES from untrusted sources or public datasets.
* **Canonicalization:** Standardize molecule representations across databases using canonical SMILES or InChIKeys.
* **Stereochemistry:** Retain crucial 3D spatial arrangements using `isomericSmiles=True`.

**Next Up in Video 02:** We will dive into **Molecular File Formats & I/O Operations** — reading and writing multi-compound SDF, MOL, SMI files, and integrating with Pandas!""")
    ]
    return create_nb(cells)

# ==============================================================================
# VIDEO 02: Molecular File Formats and I/O Operations
# ==============================================================================
def build_video_02():
    cells = [
        ("markdown", """# 🎥 Video 02: Molecular File Formats and I/O Operations
**RDKit Masterclass — From Zero to Drug Discovery AI**
* **Duration:** ~25 - 30 Minutes
* **Curriculum Level:** LEVEL 1 (Topic 06: Working with Molecular Files) & LEVEL 5 (Topic 25)
* **Target Audience:** Cheminformatics Engineers, Computational Chemists, Data Scientists

---

### ⏱️ Video Agenda & Timestamps
* **00:00 - 04:30** | Chemical File Formats Explained: SDF, MOL (V2000 vs V3000), SMI, CSV
* **04:30 - 09:30** | Reading Single Structures: `MolFromMolFile` and `MolFromMolBlock`
* **09:30 - 15:00** | High-Throughput Reading: `SDMolSupplier` vs `ForwardSDMolSupplier`
* **15:00 - 19:30** | Reading and Writing SD Tags (Metadata & Properties)
* **19:30 - 24:00** | Writing Chemical Files: `SDWriter` & `SmilesWriter`
* **24:00 - 27:30** | Pandas Integration with `PandasTools`
* **27:30 - 30:00** | Hands-On Challenge: Processing and Filtering a Multi-Compound SDF

---

### 🎯 Learning Objectives
1. Understand the anatomy of MDL MOL and SD (Structure-Data) files.
2. Read chemical files safely with `SDMolSupplier`, handling `None` molecules without halting execution.
3. Stream massive multi-gigabyte SDF files using generator-based `ForwardSDMolSupplier`.
4. Access and write property metadata tags (e.g., biological activity, compound IDs, assay results).
5. Load and save molecular datasets directly to/from Pandas DataFrames with `PandasTools`."""),

        ("code", """# Step 0: Imports and Environment Setup
import os
import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem, Draw, PandasTools
from rdkit.Chem.Draw import IPythonConsole
import pandas as pd

IPythonConsole.ipython_useSVG = True
IPythonConsole.molSize = (320, 220)

print(f"RDKit Version: {rdkit.__version__}")"""),

        ("markdown", """## 1. Anatomy of a MOL Block & V2000 Format
An MDL MOL block contains:
1. **Header Block (3 lines):** Molecule name, user/software info, comments.
2. **Counts Line:** Number of atoms, bonds, chiral flag, etc.
3. **Atom Block:** X, Y, Z coordinates and atom symbols.
4. **Bond Block:** Connected atom indices (1-indexed) and bond types.
5. **Properties/M END Line:** Indicates end of the block."""),

        ("code", """# Generate and print a MOL block for Paracetamol
paracetamol = Chem.MolFromSmiles("CC(=O)Nc1ccc(O)cc1")
AllChem.Compute2DCoords(paracetamol)
mol_block = Chem.MolToMolBlock(paracetamol)

print("=== MDL MOL BLOCK (V2000) ===")
print("\\n".join(mol_block.splitlines()[:18]))  # Print header, counts, and initial atom lines"""),

        ("markdown", """## 2. Reading Multi-Molecule SDF Files with `SDMolSupplier`
An **SDF (Structure-Data File)** bundles multiple MOL blocks separated by `$$$$`, with each molecule having associated key-value metadata tags (`> <TAG_NAME>`)."""),

        ("code", """# Create a sample SDF file in memory for practice
sample_sdf_path = "sample_drugs.sdf"

sdf_content = \"\"\"
  Aspirin
     RDKit          2D

  9  9  0  0  0  0  0  0  0  0999 V2000
    0.0000    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.2990    0.7500    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.2990    2.2500    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
    2.5981    0.0000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
    3.8971    0.7500    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    5.1962    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    5.1962   -1.5000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    3.8971   -2.2500    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    2.5981   -1.5000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0
  2  3  2  0
  2  4  1  0
  4  5  1  0
  5  6  2  0
  6  7  1  0
  7  8  2  0
  8  9  1  0
  9  4  1  0
M  END
> <COMPOUND_ID>
DRUG_001

> <TARGET_IC50_nM>
25.4

> <MECHANISM>
COX-1/COX-2 Inhibitor

$$$$
\"\"\"

with open(sample_sdf_path, "w") as f:
    f.write(sdf_content)

# Reading with SDMolSupplier
suppl = Chem.SDMolSupplier(sample_sdf_path)
print(f"Total entries in supplier: {len(suppl)}")

mol = suppl[0]
if mol:
    print(f"Loaded molecule with {mol.GetNumAtoms()} atoms.")
    print("Metadata properties:", mol.GetPropsAsDict())"""),

        ("markdown", """## 3. High-Throughput / Big Data: `ForwardSDMolSupplier`
`SDMolSupplier` indexes the entire file into memory (which fails for multi-gigabyte files like the entire ZINC or PubChem databases).
`ForwardSDMolSupplier` is a streaming generator that reads one molecule at a time from a file stream, using constant minimal memory!"""),

        ("code", """# Memory-efficient forward supplier demonstration
with open(sample_sdf_path, "rb") as f_stream:
    forward_suppl = Chem.ForwardSDMolSupplier(f_stream)
    for idx, mol in enumerate(forward_suppl):
        if mol is None:
            continue
        props = mol.GetPropsAsDict()
        print(f"Streamed Molecule {idx+1}: ID={props.get('COMPOUND_ID', 'N/A')}, IC50={props.get('TARGET_IC50_nM', 'N/A')} nM")"""),

        ("markdown", """## 4. Writing Molecules and Properties with `SDWriter`
Let's prepare multiple molecules with custom properties and export them to a new production-ready `.sdf` file."""),

        ("code", """compounds_to_export = [
    ("Erlotinib", "C#Cc1cccc(Nc2ncnc3cc(OCCOC)c(OCCOC)cc23)c1", 12.0, "Approved"),
    ("Gefitinib", "COc1cc2ncnc(Nc3ccc(F)c(Cl)c3)c2cc1OCCCN4CCOCC4", 3.2, "Approved"),
    ("Lapatinib", "CS(=O)(=O)CCNCc1ccc(o1)c2ccc3c(c2)c(c(cn3)c4cccc(c4Cl)Oc5cccc(c5)F)N", 9.8, "Approved"),
    ("Afatinib", "CN(C)C/C=C/C(=O)Nc1cc2c(Nc3ccc(Cl)c(F)c3)ncnc2cc1O[C@H]4CCOC4", 0.5, "Approved")
]

output_sdf = "kinase_inhibitors.sdf"
writer = Chem.SDWriter(output_sdf)

for name, smi, ic50, status in compounds_to_export:
    m = Chem.MolFromSmiles(smi)
    if m:
        # Generate 2D coordinates for clear visual depiction in chemical software (ChemDraw, PyMOL, Discovery Studio)
        AllChem.Compute2DCoords(m)
        
        # Set metadata properties
        m.SetProp("_Name", name)
        m.SetProp("Compound_Name", name)
        m.SetProp("SMILES", smi)
        m.SetProp("EGFR_IC50_nM", str(ic50))
        m.SetProp("Clinical_Status", status)
        
        writer.write(m)

writer.close()
print(f"✅ Successfully wrote {len(compounds_to_export)} molecules to '{output_sdf}'!")"""),

        ("markdown", """## 5. Working with SMILES Files (`SmilesMolSupplier` and `SmilesWriter`)
SMILES files (`.smi` or `.tsv`) are tab/space-separated text files containing:
`SMILES <whitespace> Molecule_Name`."""),

        ("code", """smi_file = "compounds.smi"
with open(smi_file, "w") as f:
    f.write("CC(=O)Oc1ccccc1C(=O)O Aspirin\\n")
    f.write("CC(C)Cc1ccc(cc1)C(C)C(=O)O Ibuprofen\\n")
    f.write("CC(=O)Nc1ccc(O)cc1 Paracetamol\\n")

# Reading SMILES files
smi_suppl = Chem.SmilesMolSupplier(smi_file, delimiter=" ", smilesColumn=0, nameColumn=1, titleLine=False)
for mol in smi_suppl:
    if mol:
        print(f"Read from .smi: {mol.GetProp('_Name'):<12} -> Formula: {Chem.rdMolDescriptors.CalcMolFormula(mol)}")"""),

        ("markdown", """## 6. Integration with Pandas: `PandasTools`
`rdkit.Chem.PandasTools` allows you to load SDFs into Pandas DataFrames, rendering interactive 2D structure images directly inside Jupyter tables!"""),

        ("code", """# Load our generated SDF into a Pandas DataFrame
df_sdf = PandasTools.LoadSDF(output_sdf)
print(f"DataFrame Shape: {df_sdf.shape}")
df_sdf[["Compound_Name", "EGFR_IC50_nM", "Clinical_Status", "ROMol"]].head()"""),

        ("markdown", """## 7. 🎯 Video Hands-On Challenge & Solution
### Problem:
1. Load `kinase_inhibitors.sdf` using `SDMolSupplier`.
2. Compute the Molecular Weight (MW) for each compound.
3. Add a new tag `Potency_Tier`:
   * `"High"` if `EGFR_IC50_nM < 5.0`
   * `"Moderate"` otherwise.
4. Save the annotated molecules into `kinase_inhibitors_annotated.sdf`.
5. Verify the new file by reading and printing the tags."""),

        ("code", """from rdkit.Chem import Descriptors

suppl = Chem.SDMolSupplier(output_sdf)
out_annotated = "kinase_inhibitors_annotated.sdf"
writer = Chem.SDWriter(out_annotated)

for mol in suppl:
    if mol is None:
        continue
    
    # Calculate MW
    mw = Descriptors.MolWt(mol)
    mol.SetDoubleProp("MolecularWeight", round(mw, 2))
    
    # Check potency
    ic50 = float(mol.GetProp("EGFR_IC50_nM"))
    tier = "High" if ic50 < 5.0 else "Moderate"
    mol.SetProp("Potency_Tier", tier)
    
    writer.write(mol)

writer.close()

# Verify output
verify_suppl = Chem.SDMolSupplier(out_annotated)
print("=== VERIFICATION OF ANNOTATED SDF ===")
for m in verify_suppl:
    if m:
        props = m.GetPropsAsDict()
        name = m.GetProp("_Name") if m.HasProp("_Name") else props.get("Compound_Name", "Unknown")
        print(f"Compound: {name:<12} | MW: {props.get('MolecularWeight', 'N/A')} | IC50: {props.get('EGFR_IC50_nM', 'N/A')} nM | Tier: {props.get('Potency_Tier', 'N/A')}")"""),

        ("markdown", """## 8. Summary & Best Practices
* **Use `SDMolSupplier`** when you need fast random access and the file fits in RAM.
* **Use `ForwardSDMolSupplier`** when streaming massive library downloads (millions of compounds).
* **Always call `AllChem.Compute2DCoords(mol)`** before writing to SDF so external cheminformatics tools display clean structures.
* **Use `PandasTools`** for rapid exploratory data analysis, filtering, and interactive visualization.

**Next Up in Video 03:** **Molecular Sanitization, Cleaning & Quality Control** — fixing valence errors, stripping counterion salts, and building an automated dataset curation pipeline!""")
    ]
    return create_nb(cells)

# ==============================================================================
# VIDEO 03: Molecular Sanitization and Cleaning
# ==============================================================================
def build_video_03():
    cells = [
        ("markdown", """# 🎥 Video 03: Molecular Sanitization, Cleaning & Quality Control
**RDKit Masterclass — From Zero to Drug Discovery AI**
* **Duration:** ~25 - 30 Minutes
* **Curriculum Level:** LEVEL 1 (Topic 07: Sanitization) & LEVEL 5 (Topics 26, 27, 28, 29)
* **Target Audience:** Cheminformatics Engineers, AI for Drug Discovery Researchers, Data Scientists

---

### ⏱️ Video Agenda & Timestamps
* **00:00 - 05:00** | What is Molecular Sanitization? The 8 Internal Steps
* **05:00 - 10:00** | Diagnosing Sanitization Failures (Valence errors, Aromaticity bugs)
* **10:00 - 14:30** | Debugging with `sanitize=False` and Manual Fixes
* **14:30 - 19:00** | Stripping Salts and Counterions with `SaltRemover`
* **19:00 - 23:30** | Deduplication & Resolving InChIKey Clashes
* **23:30 - 27:30** | Building an Automated Chemical Dataset Quality Control (QC) Pipeline
* **27:30 - 30:00** | Hands-On Exercise & Real Dataset Cleaning

---

### 🎯 Learning Objectives
1. Understand why RDKit rejects chemically unreasonable molecules.
2. Master the 8 sanitization operations: valence check, aromaticity perception, kekulization, etc.
3. Catch `Chem.MolSanitizeException` and debug broken molecules without crashing batch jobs.
4. Remove salts (HCl, TFA, sodium, acetate) to isolate the active pharmaceutical ingredient (API).
5. Build a production-grade QC report generator for chemical libraries."""),

        ("code", """# Step 0: Imports and Environment Setup
import rdkit
from rdkit import Chem
from rdkit.Chem import Draw, SaltRemover
from rdkit.Chem.Draw import IPythonConsole
import pandas as pd

IPythonConsole.ipython_useSVG = True
IPythonConsole.molSize = (320, 220)

print(f"RDKit Version: {rdkit.__version__}")"""),

        ("markdown", """## 1. What Happens During Sanitization?
When you call `Chem.MolFromSmiles(smi)`, RDKit by default calls `Chem.SanitizeMol(mol)`.
This executes an 8-step quality verification pipeline:
1. `SANITIZE_CLEANUP`: Cleans up non-standard representations.
2. `SANITIZE_PROPERTIES`: Calculates implicit valence and resets computed properties.
3. `SANITIZE_SYMMRINGS`: Finds symmetric rings.
4. `SANITIZE_KEKULIZE`: Checks if aromatic systems can be represented as valid Kekule structures.
5. `SANITIZE_SETCONJUGATION`: Identifies conjugated bonds.
6. `SANITIZE_SETHYBRIDIZATION`: Sets atom hybridization ($sp, sp^2, sp^3, sp^3d$).
7. `SANITIZE_CLEANUPCHIRALITY`: Removes invalid stereochemical flags.
8. `SANITIZE_ADJUSTHS`: Adds implicit hydrogens according to atomic valence rules."""),

        ("code", """# Normal sanitization in action
smi_good = "c1ccccc1O"  # Phenol
mol = Chem.MolFromSmiles(smi_good)
print("Phenol parsed and sanitized successfully!")
print(f"Oxygen hybridization: {mol.GetAtomWithIdx(6).GetHybridization()}")
print(f"Ring carbon aromaticity: {mol.GetAtomWithIdx(0).GetIsAromatic()}")"""),

        ("markdown", """## 2. Catching and Debugging Sanitization Failures
What happens when a chemist writes a 5-valent nitrogen without a formal positive charge? Or an unkekulizable aromatic ring?
RDKit fails with a `Chem.MolSanitizeException`.
Let's see how to inspect the raw molecule using `sanitize=False`!"""),

        ("code", """# A classic error: uncharged pentavalent nitrogen in a nitro group: -N(=O)=O vs -[N+](=O)[O-]
broken_nitro_smiles = "CN(=O)=O"  # Chemically incorrect valence (5 bonds on uncharged N)

# Default attempt fails and returns None
mol_failed = Chem.MolFromSmiles(broken_nitro_smiles)
print(f"Default MolFromSmiles result: {mol_failed}")

# Load without sanitization to inspect what was in the string
mol_raw = Chem.MolFromSmiles(broken_nitro_smiles, sanitize=False)
print(f"Raw loaded molecule object: {mol_raw}")
print(f"Raw atoms count: {mol_raw.GetNumAtoms()}")

# Let's catch the exact sanitization error
try:
    Chem.SanitizeMol(mol_raw)
except Chem.MolSanitizeException as e:
    print(f"🚨 Caught Expected Sanitization Error:\\n   {e}")"""),

        ("markdown", """## 3. Removing Salts and Solvents (`SaltRemover`)
In medicinal chemistry databases (e.g. ChEMBL, PubChem), molecules are often synthesized and crystallized as salts (e.g., Hydrochloride, Tartrate, Besylate, Sodium).
For molecular modeling, docking, QSAR, and ML, **we must remove salts** to retain only the parent active drug!"""),

        ("code", """# Examples of drug molecules with salt adducts
salt_molecules = [
    ("Metformin Hydrochloride", "CN(C)C(=N)NC(=N)N.Cl"),
    ("Diclofenac Sodium", "O=C([O-])Cc1ccccc1Nc2c(Cl)cccc2Cl.[Na+]"),
    ("Morphine Sulfate", "CN1CCC23C4C1CC5=C2C(=C(C=C5)O)OC3C(C=C4)O.OS(=O)(=O)O")
]

# Initialize standard RDKit SaltRemover
remover = SaltRemover.SaltRemover()

cleaned_mols = []
legends = []

for name, smi in salt_molecules:
    m = Chem.MolFromSmiles(smi)
    # Strip salt
    m_clean = remover.StripMol(m)
    
    cleaned_mols.extend([m, m_clean])
    legends.extend([f"Raw: {name}", f"Clean API: {name}"])
    
    print(f"Stripped '{name}': {m.GetNumAtoms()} atoms -> {m_clean.GetNumAtoms()} atoms (Canonical: {Chem.MolToSmiles(m_clean)})")

Draw.MolsToGridImage(cleaned_mols, legends=legends, molsPerRow=2, subImgSize=(300, 200))"""),

        ("markdown", """## 4. Alternative Fragment Splitting: Largest Fragment Chooser
Sometimes salts are unusual or not in the default dictionary. In that case, we can keep the largest organic fragment by molecular weight or heavy atom count."""),

        ("code", """def get_largest_fragment(mol):
    \"\"\"Extract the largest covalent fragment from a multi-component Mol object.\"\"\"
    frags = Chem.GetMolFrags(mol, asMols=True)
    if not frags:
        return None
    # Sort by number of heavy atoms descending
    sorted_frags = sorted(frags, key=lambda m: m.GetNumAtoms(), reverse=True)
    return sorted_frags[0]

test_smi = "CC(=O)O.Cc1ccc(cc1)S(=O)(=O)O.CN1CCN(CC1)c2ncnc3c2cc(OCC4CCCO4)c(OC)c3"
test_m = Chem.MolFromSmiles(test_smi)
parent_m = get_largest_fragment(test_m)

print(f"Original multi-component SMILES atoms: {test_m.GetNumAtoms()}")
print(f"Isolated parent API atoms:            {parent_m.GetNumAtoms()}")
print(f"Parent API SMILES:                    {Chem.MolToSmiles(parent_m)}")"""),

        ("markdown", """## 5. Deduplication & InChIKey Hashes
Real datasets contain duplicate entries due to multiple assay reports, different salt forms, or varied drawing styles.
Using **Canonical SMILES** and **InChIKeys** provides an unambiguous deduplication filter."""),

        ("code", """# Dataset with duplicates in different drawing formats
raw_records = [
    {"id": "CMPD_1", "smiles": "c1ccccc1C(=O)O"},
    {"id": "CMPD_2", "smiles": "O=C(O)c1ccccc1"},                # Duplicate of 1
    {"id": "CMPD_3", "smiles": "c1ccccc1C(=O)O.Cl"},             # Salt duplicate of 1
    {"id": "CMPD_4", "smiles": "Cc1ccc(cc1)C(=O)O"},             # Distinct (4-methylbenzoic acid)
    {"id": "CMPD_5", "smiles": "Cc1cccc(c1)C(=O)O"},             # Distinct (3-methylbenzoic acid)
]

unique_dict = {}
remover = SaltRemover.SaltRemover()

for rec in raw_records:
    mol = Chem.MolFromSmiles(rec["smiles"])
    if mol is None:
        continue
    # Strip salts
    mol = remover.StripMol(mol)
    # Generate canonical InChIKey
    ikey = Chem.MolToInchiKey(mol)
    
    if ikey not in unique_dict:
        unique_dict[ikey] = {
            "ID": rec["id"],
            "Canonical_SMILES": Chem.MolToSmiles(mol),
            "InChIKey": ikey,
            "Count": 1
        }
    else:
        unique_dict[ikey]["Count"] += 1

df_unique = pd.DataFrame(list(unique_dict.values()))
print(f"Processed {len(raw_records)} records -> {len(df_unique)} unique compounds:")
display(df_unique)"""),

        ("markdown", """## 6. Building an Automated Chemical Dataset Quality Control (QC) Pipeline
Let's assemble a complete, production-grade dataset QC class that processes any CSV/dataframe of SMILES and produces a diagnostic health report."""),

        ("code", """class ChemicalDatasetQC:
    def __init__(self):
        self.salt_remover = SaltRemover.SaltRemover()
        
    def process_dataset(self, smiles_list):
        stats = {
            "total_input": len(smiles_list),
            "valid_mols": 0,
            "invalid_smiles": 0,
            "salts_removed": 0,
            "unique_compounds": 0,
            "duplicates": 0
        }
        
        seen_keys = set()
        curated_mols = []
        
        for smi in smiles_list:
            if not isinstance(smi, str) or not smi.strip():
                stats["invalid_smiles"] += 1
                continue
                
            mol = Chem.MolFromSmiles(smi)
            if mol is None:
                stats["invalid_smiles"] += 1
                continue
                
            stats["valid_mols"] += 1
            
            # Check for salts
            num_atoms_before = mol.GetNumAtoms()
            stripped = self.salt_remover.StripMol(mol)
            if stripped.GetNumAtoms() < num_atoms_before:
                stats["salts_removed"] += 1
            
            # Check uniqueness
            ikey = Chem.MolToInchiKey(stripped)
            if ikey in seen_keys:
                stats["duplicates"] += 1
            else:
                seen_keys.add(ikey)
                curated_mols.append(stripped)
                
        stats["unique_compounds"] = len(curated_mols)
        return stats, curated_mols

# Test our QC pipeline
test_dataset = [
    "CC(=O)Oc1ccccc1C(=O)O",         # Aspirin
    "CC(=O)Oc1ccccc1C(=O)O.Na",      # Aspirin Na
    "C1=CC=CC=C1O",                  # Phenol
    "c1ccccc1O",                     # Phenol duplicate
    "C1(=O)(=O)(=O)C",               # INVALID
    "",                              # Empty string
    "CC(C)Cc1ccc(cc1)C(C)C(=O)O",    # Ibuprofen
    "CC(C)Cc1ccc(cc1)C(C)C(=O)O.Cl", # Ibuprofen HCl
]

qc = ChemicalDatasetQC()
report, clean_mols = qc.process_dataset(test_dataset)

print("=== 📊 CHEMICAL DATASET QC REPORT ===")
for k, v in report.items():
    print(f"  {k:<20}: {v}")"""),

        ("markdown", """## 7. Summary & Key Takeaways
* **Sanitization** checks valence rules, aromaticity, and ring conjugation to ensure valid chemistry.
* When molecules fail sanitization, use `sanitize=False` to inspect and diagnose the structural root cause.
* **Salt stripping** is non-negotiable in drug discovery workflows: always separate counterions from the API.
* **InChIKeys** provide robust, canonical hash keys for deduplicating compound collections.

**Next Up in Video 04:** **2D Molecular Visualization & Rendering** — atom/bond highlighting, custom color palettes, and creating publication-grade chemical figures!""")
    ]
    return create_nb(cells)

# ==============================================================================
# VIDEO 04: 2D Molecular Visualization and Rendering
# ==============================================================================
def build_video_04():
    cells = [
        ("markdown", """# 🎥 Video 04: 2D Molecular Visualization & Rendering
**RDKit Masterclass — From Zero to Drug Discovery AI**
* **Duration:** ~25 - 30 Minutes
* **Curriculum Level:** LEVEL 1 (Topic 05: Visualizing Molecules) & LEVEL 8 (Topic 47)
* **Target Audience:** Cheminformatics Engineers, Medicinal Chemists, AI Researchers

---

### ⏱️ Video Agenda & Timestamps
* **00:00 - 04:30** | Introduction: 2D Depiction Principles & Coordinate Generation
* **04:30 - 09:30** | Single Molecule Rendering: `MolToImage` & Image Sizing
* **09:30 - 15:00** | Grid Images: `MolsToGridImage` with Custom Legends and Styling
* **15:00 - 20:00** | Atom and Bond Highlighting with Custom RGB Color Schemes
* **20:00 - 25:00** | Publication-Ready Vector Graphics: `rdMolDraw2D` (SVG & Cairo)
* **25:00 - 28:00** | Visualizing Chemical Reactions
* **28:00 - 30:00** | Hands-On Challenge: Creating a High-Resolution Drug Infographic

---

### 🎯 Learning Objectives
1. Compute clear, aesthetic 2D coordinates with `rdDepictor.Compute2DCoords()`.
2. Generate professional multi-compound grid images with legends, formula, and property tags.
3. Highlight specific pharmacophore sub-structures, atoms, and bonds with custom RGB colors.
4. Export crisp, scalable SVG vector graphics suitable for papers and conference posters.
5. Depict chemical reactions with reactants, agents, and products."""),

        ("code", """# Step 0: Imports and Setup
import rdkit
from rdkit import Chem
from rdkit.Chem import Draw, rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D, IPythonConsole
from IPython.display import SVG, display
import io

IPythonConsole.ipython_useSVG = True
IPythonConsole.molSize = (350, 250)

print(f"RDKit Version: {rdkit.__version__}")"""),

        ("markdown", """## 1. Generating Aesthetic 2D Coordinates
Before rendering, 2D coordinates must be computed. RDKit uses the Riniker-Landrum 2D coordinate generation algorithm (`rdDepictor`) to produce aesthetically pleasing, standard organic chemistry layouts."""),

        ("code", """# Load Imatinib (Gleevec)
imatinib_smi = "Cc1ccc(cc1Nc2nccc(n2)c3cccnc3)NC(=O)c4ccc(cc4)CN5CCN(CC5)C"
imatinib = Chem.MolFromSmiles(imatinib_smi)

# Compute 2D coordinates explicitly
rdDepictor.Compute2DCoords(imatinib)

# Basic drawing
imatinib"""),

        ("markdown", """## 2. Advanced Multi-Compound Grid Depictions (`MolsToGridImage`)
In virtual screening, you often need to review dozens of molecules side by side.
`MolsToGridImage` allows extensive customization:
* `molsPerRow`: Number of columns.
* `subImgSize`: Pixel size of each sub-image.
* `legends`: List of string labels for each compound.
* `useSVG`: True for crystal-clear vector graphics."""),

        ("code", """kinase_drugs = {
    "Gefitinib (Iressa)": "COc1cc2ncnc(Nc3ccc(F)c(Cl)c3)c2cc1OCCCN4CCOCC4",
    "Erlotinib (Tarceva)": "C#Cc1cccc(Nc2ncnc3cc(OCCOC)c(OCCOC)cc23)c1",
    "Lapatinib (Tykerb)": "CS(=O)(=O)CCNCc1ccc(o1)c2ccc3c(c2)c(c(cn3)c4cccc(c4Cl)Oc5cccc(c5)F)N",
    "Osimertinib (Tagrisso)": "CN(C)CC=CC(=O)Nc1cc(Nc2nccc(n2)c3cn(C)c4ccccc34)c(OC)cc1N(C)CCN(C)C",
    "Sorafenib (Nexavar)": "CNC(=O)c1cc(Oc2ccc(NC(=O)Nc3ccc(Cl)c(C(F)(F)F)c3)cc2)ccn1",
    "Sunitinib (Sutent)": "CCN(CC)CCNC(=O)c1c(C)[nH]c(C=C2C(=O)Nc3ccc(F)cc23)c1C"
}

mols = [Chem.MolFromSmiles(smi) for smi in kinase_drugs.values()]
legends = list(kinase_drugs.keys())

# Render 2x3 grid
Draw.MolsToGridImage(mols, molsPerRow=3, subImgSize=(300, 200), legends=legends, useSVG=True)"""),

        ("markdown", """## 3. Highlighting Atoms and Bonds with Custom Colors
In drug discovery, you frequently want to highlight the **binding pharmacophore** or **functional group** in color.
We can pass `highlightAtoms`, `highlightBonds`, and custom RGB color dictionaries!"""),

        ("code", """# Let's find the quinazoline core substructure in Gefitinib
gefitinib = mols[0]  # Gefitinib
quinazoline_pattern = Chem.MolFromSmarts("c1ncnc2ccccc12")

matches = gefitinib.GetSubstructMatches(quinazoline_pattern)
print(f"Matched atom indices: {matches}")

matched_atoms = list(matches[0])

# Highlight the matched atoms in soft teal
highlight_colors = {idx: (0.2, 0.7, 0.8) for idx in matched_atoms}

d2d = rdMolDraw2D.MolDraw2DSVG(400, 300)
d2d.DrawMolecule(gefitinib, highlightAtoms=matched_atoms, highlightAtomColors=highlight_colors)
d2d.FinishDrawing()
SVG(d2d.GetDrawingText())"""),

        ("markdown", """## 4. Publication-Ready Vector Graphics (`rdMolDraw2D`)
For peer-reviewed journal papers, conference slides, or website banners, SVG vector format ensures infinitely scalable crisp graphics with custom styling (black background, atom numbers, thick bonds)."""),

        ("code", """# Create a customized SVG depiction
aspirin = Chem.MolFromSmiles("CC(=O)Oc1ccccc1C(=O)O")
rdDepictor.Compute2DCoords(aspirin)

drawer = rdMolDraw2D.MolDraw2DSVG(450, 300)
opts = drawer.drawOptions()

# Configure custom aesthetic options
opts.bondLineWidth = 3.0
opts.minFontSize = 12
opts.addAtomIndices = True  # Display atom numbers for reference

drawer.DrawMolecule(aspirin)
drawer.FinishDrawing()

# Display inline
SVG(drawer.GetDrawingText())"""),

        ("markdown", """## 5. Visualizing Chemical Reactions
RDKit can also render chemical reactions directly in 2D with reactants, arrows, and products!"""),

        ("code", """from rdkit.Chem import AllChem

# Amide coupling reaction: Carboxylic acid + Amine -> Amide
rxn_smarts = "[C:1](=O)[OH].[N:2][C:3]>>[C:1](=O)[N:2][C:3]"
rxn = AllChem.ReactionFromSmarts(rxn_smarts)

# Render reaction
d2d_rxn = rdMolDraw2D.MolDraw2DSVG(650, 200)
d2d_rxn.DrawReaction(rxn)
d2d_rxn.FinishDrawing()
SVG(d2d_rxn.GetDrawingText())"""),

        ("markdown", """## 6. 🎯 Video Hands-On Challenge & Solution
### Problem:
Take **Lapatinib** and **Sorafenib**:
1. Identify all aromatic ring atoms in each molecule.
2. Render both side-by-side in an SVG grid.
3. Highlight all aromatic atoms in gold/orange `(1.0, 0.75, 0.1)`.
4. Label each molecule with its drug name and number of aromatic rings."""),

        ("code", """lapatinib = Chem.MolFromSmiles(kinase_drugs["Lapatinib (Tykerb)"])
sorafenib = Chem.MolFromSmiles(kinase_drugs["Sorafenib (Nexavar)"])

pair = [lapatinib, sorafenib]
pair_legends = []
pair_highlights = []

for idx, m in enumerate(pair):
    aromatic_atoms = [atom.GetIdx() for atom in m.GetAtoms() if atom.GetIsAromatic()]
    num_arom_rings = Chem.rdMolDescriptors.CalcNumAromaticRings(m)
    
    pair_highlights.append(aromatic_atoms)
    name = "Lapatinib" if idx == 0 else "Sorafenib"
    pair_legends.append(f"{name}\\nAromatic Rings: {num_arom_rings}")

# Draw with highlights
Draw.MolsToGridImage(
    pair,
    legends=pair_legends,
    highlightAtomLists=pair_highlights,
    molsPerRow=2,
    subImgSize=(350, 250),
    useSVG=True
)"""),

        ("markdown", """## 7. Summary & Key Takeaways
* `rdDepictor.Compute2DCoords` generates aesthetically pleasing 2D organic layout coordinates.
* `MolsToGridImage` with `useSVG=True` is the fastest, cleanest way to review chemical libraries.
* `rdMolDraw2D` provides granular programmatic control over line widths, colors, atom highlights, and background transparency for publication-quality figures.

**Next Up in Video 05:** **Physicochemical Properties & Molecular Descriptors** — calculating MW, LogP, TPSA, HBD, HBA, and building an automated descriptor extraction pipeline!""")
    ]
    return create_nb(cells)

# ==============================================================================
# VIDEO 05: Physicochemical Properties and Descriptors
# ==============================================================================
def build_video_05():
    cells = [
        ("markdown", """# 🎥 Video 05: Physicochemical Properties & Molecular Descriptors
**RDKit Masterclass — From Zero to Drug Discovery AI**
* **Duration:** ~25 - 30 Minutes
* **Curriculum Level:** LEVEL 2 — Molecular Properties (Topics 08, 10, 11, 12)
* **Target Audience:** Cheminformatics Engineers, Medicinal Chemists, ML/AI Engineers

---

### ⏱️ Video Agenda & Timestamps
* **00:00 - 05:00** | What are Molecular Descriptors? 1D vs 2D vs 3D Properties
* **05:00 - 10:00** | The Core Physicochemical Profile: MW, MolLogP, TPSA, HBD, HBA, RotBonds
* **10:00 - 14:30** | Advanced Descriptors: Fraction Csp3, Ring Counts, LabuteASA, BertzCT Complexity
* **14:30 - 19:30** | Batch Descriptor Calculation: The `Descriptors._descList` Pipeline
* **19:30 - 24:30** | Statistical Distribution Analysis: Histograms, Boxplots & Outliers
* **24:30 - 28:00** | Live Coding: Building a SMILES -> Features -> CSV Pipeline
* **28:00 - 30:00** | Hands-On Exercise & Key Takeaways

---

### 🎯 Learning Objectives
1. Understand the physical meaning of LogP (lipophilicity), TPSA (permeability), and Rotatable Bonds (flexibility).
2. Calculate individual properties using `rdkit.Chem.Descriptors` and `rdMolDescriptors`.
3. Compute all ~200 RDKit 2D descriptors in an automated batch pipeline.
4. Clean and convert descriptor matrices into Pandas DataFrames for Machine Learning.
5. Visualize chemical property distributions and detect structural outliers."""),

        ("code", """# Step 0: Imports and Environment Setup
import os
import rdkit
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors, Draw
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Plotting configuration
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.figsize"] = (10, 6)

print(f"RDKit Version: {rdkit.__version__}")"""),

        ("markdown", """## 1. What are Molecular Descriptors?
A **molecular descriptor** is a numerical value that quantifies a physical, chemical, or topological feature of a molecule:
* **1D Descriptors:** Molecular weight, atom counts, molecular formula.
* **2D Descriptors:** LogP (Wildman-Crippen), Topological Polar Surface Area (TPSA), number of rotatable bonds, ring counts, shape indices.
* **3D Descriptors:** Solvent-accessible surface area, dipole moment, volume, radius of gyration (requires 3D conformers).

These descriptors form the feature foundation for **Quantitative Structure-Activity Relationship (QSAR)** modeling and **ADMET** (Absorption, Distribution, Metabolism, Excretion, Toxicity) prediction!"""),

        ("code", """# Let's inspect the core properties of Imatinib (Gleevec)
imatinib_smi = "Cc1ccc(cc1Nc2nccc(n2)c3cccnc3)NC(=O)c4ccc(cc4)CN5CCN(CC5)C"
mol = Chem.MolFromSmiles(imatinib_smi)

mw = Descriptors.MolWt(mol)
logp = Descriptors.MolLogP(mol)
tpsa = Descriptors.TPSA(mol)
hbd = Descriptors.NumHDonors(mol)
hba = Descriptors.NumHAcceptors(mol)
rot_bonds = Descriptors.NumRotatableBonds(mol)
heavy_atoms = mol.GetNumHeavyAtoms()

print(f"=== PHYSICOCHEMICAL PROFILE: IMATINIB ===")
print(f"  Molecular Weight (MW):    {mw:.2f} Da")
print(f"  Wildman-Crippen LogP:     {logp:.2f}")
print(f"  Topological Polar Area:   {tpsa:.2f} Å²")
print(f"  H-Bond Donors (HBD):      {hbd}")
print(f"  H-Bond Acceptors (HBA):   {hba}")
print(f"  Rotatable Bonds:          {rot_bonds}")
print(f"  Heavy Atom Count:         {heavy_atoms}")"""),

        ("markdown", """## 2. Advanced Structural & Complexity Descriptors
Beyond basic Lipinski properties, modern medicinal chemistry relies heavily on:
* **Fraction Csp3 (`FractionCSP3`):** Ratio of $sp^3$ hybridized carbons to total carbons. Higher Csp3 correlates with clinical trial success, better solubility, and 3D complexity ("Escape from Flatland").
* **BertzCT (`BertzCT`):** Topological index of molecular complexity.
* **LabuteASA (`LabuteASA`):** Approximate surface area.
* **Ring Counts:** Saturated, aliphatic, and aromatic ring systems."""),

        ("code", """f_csp3 = Descriptors.FractionCSP3(mol)
bertz_ct = Descriptors.BertzCT(mol)
num_rings = rdMolDescriptors.CalcNumRings(mol)
num_aromatic_rings = rdMolDescriptors.CalcNumAromaticRings(mol)
num_aliphatic_rings = rdMolDescriptors.CalcNumAliphaticRings(mol)

print(f"=== ADVANCED STRUCTURAL DESCRIPTORS ===")
print(f"  Fraction Csp3:            {f_csp3:.3f}")
print(f"  Bertz Complexity Index:   {bertz_ct:.2f}")
print(f"  Total Rings:              {num_rings}")
print(f"  Aromatic Rings:           {num_aromatic_rings}")
print(f"  Aliphatic Rings:          {num_aliphatic_rings}")"""),

        ("markdown", """## 3. High-Throughput Batch Descriptor Pipeline
RDKit provides ~210 pre-implemented descriptors in `rdkit.Chem.Descriptors._descList`.
Let's build an automated function that computes a selected or complete descriptor matrix for any list of molecules!"""),

        ("code", """# Define our target descriptor calculation function
def calculate_descriptors_dataframe(smiles_series, names_series=None):
    \"\"\"
    Converts a pandas Series of SMILES into a full physicochemical descriptor DataFrame.
    \"\"\"
    records = []
    
    for idx, smi in enumerate(smiles_series):
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            continue
            
        record = {
            "SMILES": smi,
            "Name": names_series.iloc[idx] if names_series is not None else f"Mol_{idx+1}",
            "MW": Descriptors.MolWt(mol),
            "LogP": Descriptors.MolLogP(mol),
            "TPSA": Descriptors.TPSA(mol),
            "HBD": Descriptors.NumHDonors(mol),
            "HBA": Descriptors.NumHAcceptors(mol),
            "RotatableBonds": Descriptors.NumRotatableBonds(mol),
            "HeavyAtoms": mol.GetNumHeavyAtoms(),
            "FractionCSP3": Descriptors.FractionCSP3(mol),
            "NumRings": rdMolDescriptors.CalcNumRings(mol),
            "AromaticRings": rdMolDescriptors.CalcNumAromaticRings(mol),
            "BertzCT": Descriptors.BertzCT(mol)
        }
        records.append(record)
        
    return pd.DataFrame(records)"""),

        ("markdown", """## 4. Profiling a Real Drug Dataset
Let's load the ChEMBL EGFR compound dataset and calculate descriptor distributions."""),

        ("code", """# Load real dataset
candidate_paths = [
    "datasets/EGFR_compounds.csv",
    "../datasets/EGFR_compounds.csv",
    "../../datasets/EGFR_compounds.csv",
    os.path.expanduser("~/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/datasets/EGFR_compounds.csv")
]
csv_path = None
for p in candidate_paths:
    if os.path.exists(p):
        csv_path = p
        break

if csv_path:
    df_raw = pd.read_csv(csv_path).head(100) # Sample 100 for fast demonstration
    df_desc = calculate_descriptors_dataframe(df_raw["smiles"], df_raw["molecule_chembl_id"])
    print(f"✅ Successfully calculated descriptors for {len(df_desc)} compounds from {csv_path}!")
    display(df_desc.head())
else:
    print("Dataset path not found. Please verify datasets/ directory.")"""),

        ("markdown", """## 5. Statistical Distribution Analysis & Outlier Detection
Let's visualize the property distributions using histograms and kernel density estimation (KDE)."""),

        ("code", """# Plot 4 key property distributions
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

sns.histplot(df_desc["MW"], kde=True, ax=axes[0, 0], color="#2b5c8f")
axes[0, 0].set_title("Molecular Weight (MW) Distribution")
axes[0, 0].set_xlabel("MW (Da)")

sns.histplot(df_desc["LogP"], kde=True, ax=axes[0, 1], color="#e07a5f")
axes[0, 1].set_title("Wildman-Crippen LogP Distribution")
axes[0, 1].set_xlabel("LogP")

sns.histplot(df_desc["TPSA"], kde=True, ax=axes[1, 0], color="#3d405b")
axes[1, 0].set_title("Topological Polar Surface Area (TPSA)")
axes[1, 0].set_xlabel("TPSA (Å²)")

sns.histplot(df_desc["FractionCSP3"], kde=True, ax=axes[1, 1], color="#81b29a")
axes[1, 1].set_title("Fraction Csp3 Distribution")
axes[1, 1].set_xlabel("Fraction Csp3")

plt.tight_layout()
plt.show()"""),

        ("markdown", """## 6. Correlation Heatmap
Let's see how properties correlate with one another (e.g. MW vs TPSA vs Heavy Atoms)."""),

        ("code", """# Correlation matrix
numeric_cols = ["MW", "LogP", "TPSA", "HBD", "HBA", "RotatableBonds", "FractionCSP3", "BertzCT"]
corr = df_desc[numeric_cols].corr()

plt.figure(figsize=(9, 7))
sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, fmt=".2f", linewidths=0.5)
plt.title("Physicochemical Descriptor Correlation Matrix")
plt.show()"""),

        ("markdown", """## 7. 🎯 Video Hands-On Challenge & Solution
### Problem:
1. Filter the dataset to find all compounds that have:
   * `MW < 450`
   * `LogP < 4.0`
   * `FractionCSP3 > 0.25`
2. Identify the top 3 most structurally complex molecules according to `BertzCT`.
3. Display their names, properties, and 2D structures."""),

        ("code", """# 1. Filter criteria
filtered_df = df_desc[
    (df_desc["MW"] < 450) & 
    (df_desc["LogP"] < 4.0) & 
    (df_desc["FractionCSP3"] > 0.25)
]

print(f"Found {len(filtered_df)} compounds meeting the stringent lead-like criteria!")

# 2. Top 3 most complex
top_complex = df_desc.sort_values(by="BertzCT", ascending=False).head(3)
print("\\nTop 3 Most Complex Compounds (BertzCT):")
display(top_complex[["Name", "MW", "LogP", "BertzCT", "NumRings"]])

# 3. Draw structures
top_mols = [Chem.MolFromSmiles(s) for s in top_complex["SMILES"]]
top_legends = [f"{row['Name']}\\nBertz: {row['BertzCT']:.1f}" for _, row in top_complex.iterrows()]
Draw.MolsToGridImage(top_mols, legends=top_legends, molsPerRow=3, subImgSize=(300, 200))"""),

        ("markdown", """## 8. Summary & Key Takeaways
* **`Descriptors.MolWt`, `MolLogP`, `TPSA`, `NumHDonors`, `NumHAcceptors`** form the bedrock of drug property calculations.
* **Fraction Csp3** reflects three-dimensionality and saturation — critical for solubility and target selectivity.
* **Correlations:** MW and Heavy Atoms are strongly collinear; LogP and TPSA often show inverse relationships.
* Automated descriptor pipelines allow effortless feature generation for downstream machine learning.

**Next Up in Video 06:** **Drug-Likeness Rules & MedChem Filters** — Lipinski's Rule of 5, Veber's criteria, and filtering toxicophores with PAINS and Brenk alerts!""")
    ]
    return create_nb(cells)

# ==============================================================================
# MAIN RUNNER FOR VIDEOS 01 TO 05
# ==============================================================================
if __name__ == "__main__":
    base_dir = "/home/softvence/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/RDKit Tutorials"
    
    video_configs = [
        ("01_Molecule_Representation/Video_01_RDKit_Fundamentals_and_Molecular_Objects.ipynb", build_video_01),
        ("02_SMILES_MOL_SDF_Handling/Video_02_Molecular_File_Formats_and_IO.ipynb", build_video_02),
        ("03_Data_Loading_and_Cleaning/Video_03_Molecular_Sanitization_and_Cleaning.ipynb", build_video_03),
        ("13_Molecular_Visualization/Video_04_2D_Molecular_Visualization_and_Rendering.ipynb", build_video_04),
        ("04_Molecular_Descriptors_and_Properties/Video_05_Physicochemical_Properties_and_Descriptors.ipynb", build_video_05)
    ]
    
    for rel_path, builder_func in video_configs:
        full_path = os.path.join(base_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        nb = builder_func()
        with open(full_path, "w", encoding="utf-8") as f:
            nbf.write(nb, f)
        print(f"Generated: {rel_path} ({len(nb.cells)} cells)")
