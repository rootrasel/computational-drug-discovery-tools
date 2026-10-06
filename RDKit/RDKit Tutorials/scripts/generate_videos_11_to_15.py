#!/usr/bin/env python3
"""
Generator script for Video Tutorials 11 to 15 of the RDKit Master Playlist.
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
# VIDEO 11: Chemical Space Exploration, Dimensionality Reduction & Clustering
# ==============================================================================
def build_video_11():
    cells = [
        ("markdown", """# 🎥 Video 11: Chemical Space Exploration, Dimensionality Reduction & Clustering
**RDKit Masterclass — From Zero to Drug Discovery AI**
* **Duration:** ~25 - 30 Minutes
* **Curriculum Level:** LEVEL 6 — Chemical Space Exploration (Topics 30, 31, 32, 33, 34, 35)
* **Target Audience:** Cheminformatics Engineers, AI Researchers, Screening Scientists

---

### ⏱️ Video Agenda & Timestamps
* **00:00 - 05:00** | What is Chemical Space? High-Dimensional Fingerprint Manifolds
* **05:00 - 10:00** | Dimensionality Reduction: PCA vs t-SNE (Global Variance vs Local Neighborhoods)
* **10:00 - 15:00** | Visualizing Chemical Space Colored by Bioactivity ($pIC_{50}$) & Physicochemical Properties
* **15:00 - 20:00** | Molecular Clustering: Taylor-Butina Clustering (The Gold Standard)
* **20:00 - 24:30** | Extracting Cluster Centroids & Structural Diversity Analysis
* **24:30 - 28:00** | Diverse Subset Selection via `MaxMinPicker`
* **28:00 - 30:00** | Hands-On Challenge & Summary

---

### 🎯 Learning Objectives
1. Project 2048-dimensional Morgan fingerprints into 2D chemical space using PCA and t-SNE.
2. Color-code chemical space projections by bioactivity ($pIC_{50}$) and molecular weight to detect SAR clusters.
3. Master **Taylor-Butina sphere exclusion clustering** (`rdkit.ML.Cluster.Butina`).
4. Identify representative cluster centroids and inspect scaffold diversity.
5. Select diverse representative subsets of compounds for wet-lab screening using `MaxMinPicker`."""),

        ("code", """# Step 0: Imports and Setup
import os
import rdkit
from rdkit import Chem
from rdkit.Chem import Draw, rdFingerprintGenerator, Descriptors
from rdkit import DataStructs
from rdkit.ML.Cluster import Butina
from rdkit.SimDivFilters.rdSimDivPickers import MaxMinPicker
from rdkit.Chem.Draw import IPythonConsole
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

IPythonConsole.ipython_useSVG = True

print(f"RDKit Version: {rdkit.__version__}")"""),

        ("markdown", """## 1. Loading the Chemical Library & Featurization
We load our real ChEMBL EGFR compound dataset with measured $pIC_{50}$ bioactivity values and generate 1024-bit Morgan fingerprints (ECFP4)."""),

        ("code", """candidate_paths = [
    "datasets/EGFR_compounds.csv",
    "../datasets/EGFR_compounds.csv",
    "../../datasets/EGFR_compounds.csv",
    os.path.expanduser("~/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/datasets/EGFR_compounds.csv")
]
csv_path = next((p for p in candidate_paths if os.path.exists(p)), None)

if csv_path:
    df_raw = pd.read_csv(csv_path).head(400) # Sample 400 compounds for fast rendering
    
    mols = []
    valid_records = []
    mfpgen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=1024)
    fps = []
    
    for idx, row in df_raw.iterrows():
        m = Chem.MolFromSmiles(row["smiles"])
        if m:
            mols.append(m)
            fps.append(mfpgen.GetFingerprint(m))
            valid_records.append({
                "ChEMBL_ID": row["molecule_chembl_id"],
                "SMILES": row["smiles"],
                "pIC50": row.get("pIC50", np.nan),
                "MW": Descriptors.MolWt(m),
                "LogP": Descriptors.MolLogP(m)
            })
            
    df_chem = pd.DataFrame(valid_records)
    print(f"✅ Prepared {len(mols)} valid molecules with ECFP4 fingerprints.")"""),

        ("markdown", """## 2. Dimensionality Reduction: PCA vs t-SNE
* **PCA (Principal Component Analysis):** Linear projection maximizing global variance.
* **t-SNE (t-Distributed Stochastic Neighbor Embedding):** Non-linear projection preserving local neighborhood topologies (structurally similar molecules group tightly into visual clusters)."""),

        ("code", """# Convert bit vectors to dense numpy matrix
X_fp = np.zeros((len(fps), 1024), dtype=np.float32)
for i, fp in enumerate(fps):
    DataStructs.ConvertToNumpyArray(fp, X_fp[i])

# 1. PCA
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_fp)

# 2. t-SNE
tsne = TSNE(n_components=2, random_state=42, perplexity=25, max_iter=1000)
X_tsne = tsne.fit_transform(X_fp)

df_chem["PCA_1"] = X_pca[:, 0]
df_chem["PCA_2"] = X_pca[:, 1]
df_chem["tSNE_1"] = X_tsne[:, 0]
df_chem["tSNE_2"] = X_tsne[:, 1]

print(f"PCA explained variance ratio (PC1 + PC2): {pca.explained_variance_ratio_.sum():.2%}")"""),

        ("markdown", """## 3. Visualizing Chemical Space Colored by Bioactivity ($pIC_{50}$)
Let's see if active compounds ($pIC_{50} \\ge 8.0$) cluster together in chemical space!"""),

        ("code", """fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Plot PCA
sc1 = axes[0].scatter(df_chem["PCA_1"], df_chem["PCA_2"], c=df_chem["pIC50"], cmap="viridis", alpha=0.8, s=40)
axes[0].set_title("Chemical Space (PCA) colored by pIC50", fontsize=13)
axes[0].set_xlabel("Principal Component 1")
axes[0].set_ylabel("Principal Component 2")
fig.colorbar(sc1, ax=axes[0], label="pIC50 (Potency)")

# Plot t-SNE
sc2 = axes[1].scatter(df_chem["tSNE_1"], df_chem["tSNE_2"], c=df_chem["pIC50"], cmap="plasma", alpha=0.8, s=40)
axes[1].set_title("Chemical Space (t-SNE) colored by pIC50", fontsize=13)
axes[1].set_xlabel("t-SNE Dimension 1")
axes[1].set_ylabel("t-SNE Dimension 2")
fig.colorbar(sc2, ax=axes[1], label="pIC50 (Potency)")

plt.tight_layout()
plt.show()"""),

        ("markdown", """## 4. Taylor-Butina Molecular Clustering
The **Taylor-Butina algorithm** is the industry standard for chemical library clustering:
1. Calculates all pairwise Tanimoto distances: $d(A, B) = 1 - T(A, B)$.
2. For each molecule, counts the number of neighbors within a defined distance cutoff (sphere radius, e.g. $0.35$ or $0.40$).
3. Sorts molecules by neighbor count descending.
4. The molecule with the most neighbors becomes the **centroid** of Cluster 1, and its neighbors are placed in Cluster 1 and removed from the pool.
5. Repeats until all molecules are assigned to clusters or singletons!"""),

        ("code", """# Compute condensed distance matrix (1D list of lower triangle)
n_mols = len(fps)
dists = []
for i in range(1, n_mols):
    sims = DataStructs.BulkTanimotoSimilarity(fps[i], fps[:i])
    dists.extend([1.0 - x for x in sims])

# Run Butina clustering with distance cutoff = 0.35 (Tanimoto similarity >= 0.65)
dist_cutoff = 0.35
clusters = Butina.ClusterData(dists, n_mols, dist_cutoff, isDistData=True)

print(f"Total Clusters Formed: {len(clusters)}")
print(f"Largest Cluster Size:  {len(clusters[0])} molecules")
print(f"Singletons (size=1):   {sum(1 for c in clusters if len(c) == 1)}")"""),

        ("markdown", """## 5. Visualizing Cluster Centroids
The centroid of each cluster represents the core structural scaffold of that chemical family."""),

        ("code", """# Display the top 4 cluster centroids (most populated chemical families)
top_clusters = clusters[:4]
centroid_mols = [mols[c[0]] for c in top_clusters]
centroid_legends = [
    f"Cluster #{i+1}\\n({len(c)} compounds)\\n{df_chem.iloc[c[0]]['ChEMBL_ID']}"
    for i, c in enumerate(top_clusters)
]

Draw.MolsToGridImage(centroid_mols, legends=centroid_legends, molsPerRow=4, subImgSize=(280, 220))"""),

        ("markdown", """## 6. Diverse Subset Selection with `MaxMinPicker`
When cherry-picking a diverse subset of $N$ compounds to purchase or test in high-throughput screening, `MaxMinPicker` iteratively selects the molecule whose minimum distance to the already selected set is maximized."""),

        ("code", """picker = MaxMinPicker()
num_diverse_picks = 5

# LazyBitVectorPick selects diverse compounds directly from fingerprints
picked_indices = list(picker.LazyBitVectorPick(fps, n_mols, num_diverse_picks, seed=42))
print("MaxMin Selected Diverse Compound Indices:", picked_indices)

diverse_mols = [mols[idx] for idx in picked_indices]
diverse_legends = [f"Diverse #{i+1}\\n{df_chem.iloc[idx]['ChEMBL_ID']}" for i, idx in enumerate(picked_indices)]

Draw.MolsToGridImage(diverse_mols, legends=diverse_legends, molsPerRow=5, subImgSize=(260, 200))"""),

        ("markdown", """## 7. 🎯 Video Hands-On Challenge & Solution
### Problem:
1. Re-cluster the library with a tighter distance cutoff of $0.25$ (Tanimoto $\\ge 0.75$).
2. How does the number of clusters change?
3. Calculate the average $pIC_{50}$ for compounds belonging to Cluster 1."""),

        ("code", """clusters_tight = Butina.ClusterData(dists, n_mols, 0.25, isDistData=True)
print(f"Clusters with cutoff 0.25: {len(clusters_tight)} (vs {len(clusters)} with cutoff 0.35)")

cluster_1_indices = clusters_tight[0]
c1_pic50s = df_chem.iloc[list(cluster_1_indices)]["pIC50"].dropna()

print(f"Cluster 1 compound count: {len(cluster_1_indices)}")
print(f"Cluster 1 Mean pIC50:     {c1_pic50s.mean():.2f}")
print(f"Cluster 1 Std Dev pIC50:  {c1_pic50s.std():.2f}")"""),

        ("markdown", """## 8. Summary & Key Takeaways
* **Chemical space projections** (t-SNE) reveal SAR islands: structurally related analogs clustered together with similar potencies.
* **Taylor-Butina Clustering** is fast, deterministic, and does not require pre-specifying $K$ (unlike K-Means).
* **`MaxMinPicker`** guarantees optimal chemical diversity for library design and screening deck cherry-picking.

**Next Up in Video 12:** **Bemis-Murcko Scaffolds & Molecular Decomposition** — core scaffold extraction, framework hopping, and matched molecular pair analysis!""")
    ]
    return create_nb(cells)

# ==============================================================================
# VIDEO 12: Bemis-Murcko Scaffolds & Molecular Decomposition
# ==============================================================================
def build_video_12():
    cells = [
        ("markdown", """# 🎥 Video 12: Bemis-Murcko Scaffolds & Molecular Decomposition
**RDKit Masterclass — From Zero to Drug Discovery AI**
* **Duration:** ~25 - 30 Minutes
* **Curriculum Level:** LEVEL 8 — Advanced RDKit (Topics 44, 45, 46)
* **Target Audience:** Medicinal Chemists, Cheminformatics Engineers, AI Researchers

---

### ⏱️ Video Agenda & Timestamps
* **00:00 - 04:30** | Bemis-Murcko Scaffold Theory: Rings, Linkers, and Side Chains
* **04:30 - 09:30** | Extracting Murcko Scaffolds with `MurckoScaffold.GetScaffoldForMol`
* **09:30 - 14:00** | Generic Scaffolds (Carbon Skeletons): `MakeScaffoldGeneric`
* **14:00 - 19:30** | Scaffold Frequency Analysis in the ChEMBL EGFR Dataset
* **19:30 - 24:30** | Scaffold Diversity Metrics & Cumulative Frequency Curves
* **24:30 - 27:30** | Scaffold Hopping & Introduction to Matched Molecular Pairs (MMP)
* **27:30 - 30:00** | Hands-On Challenge & Summary

---

### 🎯 Learning Objectives
1. Deconstruct small molecules into Bemis-Murcko scaffolds, linkers, and side chains.
2. Abstract heteroatoms and bond orders into generic carbon frameworks.
3. Perform library-wide scaffold frequency profiling to detect privileged drug cores.
4. Quantify chemical diversity using scaffold-to-compound ratios.
5. Understand scaffold hopping and how Matched Molecular Pairs identify activity cliffs."""),

        ("code", """# Step 0: Imports and Setup
import os
import rdkit
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Scaffolds import MurckoScaffold
from rdkit.Chem.Draw import IPythonConsole
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

IPythonConsole.ipython_useSVG = True

print(f"RDKit Version: {rdkit.__version__}")"""),

        ("markdown", """## 1. Bemis-Murcko Scaffold Theory
In 1996, Guy Bemis and Mark Murcko (Vertex Pharmaceuticals) proposed decomposing any drug molecule into 4 components:
1. **Rings:** Cyclic systems.
2. **Linkers:** Acyclic chains connecting two or more rings.
3. **Scaffold:** The union of all rings and linkers (the core molecular architecture).
4. **Side Chains:** Non-ring substituents attached to the scaffold.

A **Generic Scaffold** further abstracts all atoms to carbon and all bonds to single bonds, exposing the pure topological carbon skeleton!"""),

        ("code", """# Example: Gefitinib (Iressa)
gefitinib_smi = "COc1cc2ncnc(Nc3ccc(F)c(Cl)c3)c2cc1OCCCN4CCOCC4"
gefitinib = Chem.MolFromSmiles(gefitinib_smi)

# 1. Extract standard Murcko scaffold
scaffold = MurckoScaffold.GetScaffoldForMol(gefitinib)

# 2. Extract generic framework (carbon skeleton)
generic_scaffold = MurckoScaffold.MakeScaffoldGeneric(scaffold)

print("Original SMILES:        ", gefitinib_smi)
print("Murcko Scaffold SMILES: ", Chem.MolToSmiles(scaffold))
print("Generic Framework:      ", Chem.MolToSmiles(generic_scaffold))

Draw.MolsToGridImage(
    [gefitinib, scaffold, generic_scaffold],
    legends=["Full Drug (Gefitinib)", "Bemis-Murcko Scaffold", "Generic Framework (Topology)"],
    molsPerRow=3,
    subImgSize=(300, 220)
)"""),

        ("markdown", """## 2. Library-Scale Scaffold Frequency Analysis
In drug discovery campaigns, we want to know:
* What are the most common privileged scaffolds?
* Is our library structurally diverse or dominated by a single chemical family?"""),

        ("code", """# Load EGFR dataset
candidate_paths = [
    "datasets/EGFR_compounds.csv",
    "../datasets/EGFR_compounds.csv",
    "../../datasets/EGFR_compounds.csv",
    os.path.expanduser("~/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/datasets/EGFR_compounds.csv")
]
csv_path = next((p for p in candidate_paths if os.path.exists(p)), None)

if csv_path:
    df_egfr = pd.read_csv(csv_path).head(500)
    scaffold_counts = {}
    
    for smi in df_egfr["smiles"]:
        m = Chem.MolFromSmiles(smi)
        if m:
            scaff = MurckoScaffold.GetScaffoldForMol(m)
            scaff_smi = Chem.MolToSmiles(scaff)
            scaffold_counts[scaff_smi] = scaffold_counts.get(scaff_smi, 0) + 1
            
    df_scaffolds = pd.DataFrame(list(scaffold_counts.items()), columns=["Scaffold_SMILES", "Frequency"])
    df_scaffolds = df_scaffolds.sort_values(by="Frequency", ascending=False).reset_index(drop=True)
    
    print(f"Total Compounds Processed: {len(df_egfr)}")
    print(f"Total Unique Scaffolds:    {len(df_scaffolds)}")
    print(f"Scaffold-to-Compound Ratio: {len(df_scaffolds)/len(df_egfr):.3f}")
    display(df_scaffolds.head(5))"""),

        ("markdown", """## 3. Visualizing the Top Privileged Scaffolds
Let's render the top 4 most common structural scaffolds across our compound library."""),

        ("code", """top_scaff_mols = [Chem.MolFromSmiles(s) for s in df_scaffolds["Scaffold_SMILES"].head(4)]
top_scaff_legends = [
    f"Rank #{i+1}\\nCount: {row['Frequency']}\\n({row['Frequency']/len(df_egfr):.1%})"
    for i, row in df_scaffolds.head(4).iterrows()
]

Draw.MolsToGridImage(top_scaff_mols, legends=top_scaff_legends, molsPerRow=4, subImgSize=(280, 220))"""),

        ("markdown", """## 4. Cumulative Scaffold Diversity Curve
A diverse chemical library has a gradual cumulative curve, whereas a focused/biased library plateaus rapidly."""),

        ("code", """df_scaffolds["Cumulative_Percent"] = df_scaffolds["Frequency"].cumsum() / df_scaffolds["Frequency"].sum() * 100

plt.figure(figsize=(9, 5))
plt.plot(range(1, len(df_scaffolds) + 1), df_scaffolds["Cumulative_Percent"], color="#2b5c8f", linewidth=2.5)
plt.axhline(50, color="red", linestyle="--", label="50% of Library")
plt.xlabel("Number of Scaffolds")
plt.ylabel("Cumulative % of Compounds")
plt.title("Cumulative Scaffold Diversity Curve")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()"""),

        ("markdown", """## 5. Scaffold Hopping & Matched Molecular Pairs (MMP)
* **Scaffold Hopping:** Replacing the core central scaffold with a completely different ring system while maintaining key 3D pharmacophore interaction vectors.
* **Matched Molecular Pairs (MMP):** Two molecules that differ by only a single well-defined chemical transformation (e.g. $-H \\to -Cl$ or $-OCH_3 \\to -CF_3$).
* **Activity Cliffs:** When an MMP shows an enormous change in potency ($>100\\times$), revealing critical protein binding pockets!"""),

        ("code", """# Example of Matched Molecular Pair (Activity Cliff demonstration)
pair_1 = Chem.MolFromSmiles("COc1cc2ncnc(Nc3cccc(c3)Br)c2cc1OC") # 4-anilinoquinazoline with Br: IC50 = 3 nM
pair_2 = Chem.MolFromSmiles("COc1cc2ncnc(Nc3cccc(c3)C)c2cc1OC")  # Same scaffold with Methyl: IC50 = 850 nM

Draw.MolsToGridImage(
    [pair_1, pair_2],
    legends=["Analog A: -Br (IC50 = 3 nM)", "Analog B: -Me (IC50 = 850 nM)\\n280x Activity Cliff!"],
    molsPerRow=2,
    subImgSize=(350, 240)
)"""),

        ("markdown", """## 6. 🎯 Video Hands-On Challenge & Solution
### Problem:
Take 3 blockbuster cancer drugs:
* **Imatinib**
* **Sorafenib**
* **Erlotinib**
1. Extract their Bemis-Murcko scaffolds.
2. Extract their generic frameworks.
3. Compare their scaffold heavy atom counts and ring counts in a summary table."""),

        ("code", """test_drugs = {
    "Imatinib": "Cc1ccc(cc1Nc2nccc(n2)c3cccnc3)NC(=O)c4ccc(cc4)CN5CCN(CC5)C",
    "Sorafenib": "CNC(=O)c1cc(Oc2ccc(NC(=O)Nc3ccc(Cl)c(C(F)(F)F)c3)cc2)ccn1",
    "Erlotinib": "C#Cc1cccc(Nc2ncnc3cc(OCCOC)c(OCCOC)cc23)c1"
}

scaff_results = []
draw_mols = []
draw_legends = []

for name, smi in test_drugs.items():
    mol = Chem.MolFromSmiles(smi)
    scaff = MurckoScaffold.GetScaffoldForMol(mol)
    generic = MurckoScaffold.MakeScaffoldGeneric(scaff)
    
    scaff_results.append({
        "Drug": name,
        "Full_Atoms": mol.GetNumAtoms(),
        "Scaffold_Atoms": scaff.GetNumAtoms(),
        "Scaffold_Rings": Chem.rdMolDescriptors.CalcNumRings(scaff),
        "Scaffold_SMILES": Chem.MolToSmiles(scaff)
    })
    
    draw_mols.extend([mol, scaff, generic])
    draw_legends.extend([f"{name} (Full)", f"{name} (Scaffold)", f"{name} (Generic)"])

df_res = pd.DataFrame(scaff_results)
print("=== 🔬 SCAFFOLD DECOMPOSITION SUMMARY ===")
display(df_res[["Drug", "Full_Atoms", "Scaffold_Atoms", "Scaffold_Rings"]])

Draw.MolsToGridImage(draw_mols, legends=draw_legends, molsPerRow=3, subImgSize=(300, 200))"""),

        ("markdown", """## 7. Summary & Key Takeaways
* **Bemis-Murcko Scaffolds** filter out decorative substituents to reveal the core chemical skeleton.
* **Generic Scaffolds** enable topology-level scaffold hopping across different heteroatom systems.
* Scaffold analysis is essential for **Scaffold-based Machine Learning Splits** (Video 15) to prevent artificial data leakage!

**Next Up in Video 13:** **Chemical Reactions & BRICS-Based Molecular Design** — virtual reaction enumeration and fragment-based drug design!""")
    ]
    return create_nb(cells)

# ==============================================================================
# VIDEO 13: Chemical Reactions & BRICS-Based Molecular Design
# ==============================================================================
def build_video_13():
    cells = [
        ("markdown", """# 🎥 Video 13: Chemical Reactions & BRICS-Based Molecular Design
**RDKit Masterclass — From Zero to Drug Discovery AI**
* **Duration:** ~25 - 30 Minutes
* **Curriculum Level:** LEVEL 8 — Advanced RDKit (Topics 41, 42, 43)
* **Target Audience:** Medicinal Chemists, Computational Chemists, AI Drug Designers

---

### ⏱️ Video Agenda & Timestamps
* **00:00 - 04:30** | Reaction SMARTS: The Language of Chemical Transformations
* **04:30 - 09:30** | Creating Reactions with `AllChem.ReactionFromSmarts` & `rxn.RunReactants`
* **09:30 - 14:30** | Virtual Combinatorial Library Enumeration (Amide Couplings, Click Chemistry)
* **14:30 - 19:30** | Molecular Fragmentation: BRICS (Bioisosteric Replacement Initiated by Chemical Substructures)
* **19:30 - 24:30** | Fragment-Based Molecular Assembly: Designing New Molecules with `BRICSBuild`
* **24:30 - 28:00** | Applying Drug-Likeness Filters to Generated Virtual Libraries
* **28:00 - 30:00** | Hands-On Challenge & Summary

---

### 🎯 Learning Objectives
1. Write and interpret Reaction SMARTS with reactant and product atom-mapping numbers (`:1`, `:2`).
2. Run virtual organic reactions and handle multiple stereoisomeric/regiochemical products.
3. Enumerate combinatorial libraries from sets of building blocks (acids $\\times$ amines).
4. Fragment drug molecules along 16 retrosynthetically sensible BRICS cleavage rules.
5. Generate novel drug-like molecules computationally using BRICS fragment assembly."""),

        ("code", """# Step 0: Imports and Setup
import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem, Draw, BRICS, Descriptors
from rdkit.Chem.Draw import IPythonConsole
import pandas as pd

IPythonConsole.ipython_useSVG = True

print(f"RDKit Version: {rdkit.__version__}")"""),

        ("markdown", """## 1. Reaction SMARTS Fundamentals
A chemical reaction in SMARTS format is defined as:
`Reactant_1 . Reactant_2 >> Product_1 . Product_2`
Numbers after colons (`:1`, `:2`) are **atom-mapping indices** that track which reactant atoms map to which product atoms!

### Common Reaction: Amide Bond Coupling
Carboxylic acid + Primary/Secondary Amine $\\to$ Amide:
`[C:1](=O)[OH].[N:2][C:3] >> [C:1](=O)[N:2][C:3]`"""),

        ("code", """# Compile amide coupling reaction
amide_rxn_smarts = "[C:1](=O)[O;H1].[NX3;H2,H1:2]>>[C:1](=O)[N:2]"
rxn = AllChem.ReactionFromSmarts(amide_rxn_smarts)

# Define reactants: Benzoic acid + Ethylamine
acid = Chem.MolFromSmiles("c1ccccc1C(=O)O")
amine = Chem.MolFromSmiles("CCN")

# Run reaction
products = rxn.RunReactants((acid, amine))

print(f"Number of product trajectories: {len(products)}")
product_mol = products[0][0]
print("Product SMILES:", Chem.MolToSmiles(product_mol))

Draw.MolsToGridImage([acid, amine, product_mol], legends=["Carboxylic Acid", "Amine", "Amide Product"])"""),

        ("markdown", """## 2. Combinatorial Library Enumeration
Let's assemble a virtual combinatorial library by reacting 3 carboxylic acids with 3 amines ($3 \\times 3 = 9$ virtual products)!"""),

        ("code", """acids = [
    ("Benzoic Acid", "c1ccccc1C(=O)O"),
    ("Ibuprofen", "CC(C)Cc1ccc(cc1)C(C)C(=O)O"),
    ("Nicotinic Acid", "c1cnccc1C(=O)O")
]

amines = [
    ("Morpholine", "C1COCCN1"),
    ("Cyclopropylamine", "C1CC1N"),
    ("Aniline", "c1ccccc1N")
]

virtual_library = []
library_mols = []
library_legends = []

for a_name, a_smi in acids:
    mol_a = Chem.MolFromSmiles(a_smi)
    for b_name, b_smi in amines:
        mol_b = Chem.MolFromSmiles(b_smi)
        prod_sets = rxn.RunReactants((mol_a, mol_b))
        
        if prod_sets:
            prod = prod_sets[0][0]
            Chem.SanitizeMol(prod)
            prod_smi = Chem.MolToSmiles(prod)
            mw = Descriptors.MolWt(prod)
            logp = Descriptors.MolLogP(prod)
            
            virtual_library.append({
                "Acid": a_name,
                "Amine": b_name,
                "Product_SMILES": prod_smi,
                "MW": round(mw, 2),
                "LogP": round(logp, 2)
            })
            library_mols.append(prod)
            library_legends.append(f"{a_name[:6]}+{b_name[:6]}\\nMW:{mw:.1f}")

df_virtual = pd.DataFrame(virtual_library)
print(f"✅ Successfully enumerated {len(df_virtual)} virtual amide compounds!")
display(df_virtual.head(5))

Draw.MolsToGridImage(library_mols[:6], legends=library_legends[:6], molsPerRow=3, subImgSize=(300, 200))"""),

        ("markdown", """## 3. BRICS Molecular Fragmentation
**BRICS (Bioisosteric Replacement Initiated by Chemical Substructures):**
Decomposes molecules into synthetically accessible fragments by cleaving bonds matching 16 common chemical reactions (e.g. amides, esters, aromatic C-N, ring-spiro bonds).
Each fragment retains dummy isotope labels (e.g., `[1*]`, `[5*]`) indicating its compatible connection points!"""),

        ("code", """# Fragment Imatinib using BRICS
imatinib_smi = "Cc1ccc(cc1Nc2nccc(n2)c3cccnc3)NC(=O)c4ccc(cc4)CN5CCN(CC5)C"
imatinib = Chem.MolFromSmiles(imatinib_smi)

# Break BRICS bonds
brics_frags = BRICS.BreakBRICSBonds(imatinib)
frag_list = Chem.GetMolFrags(brics_frags, asMols=True)

print(f"Imatinib decomposed into {len(frag_list)} BRICS fragments:")
frag_smiles = [Chem.MolToSmiles(f) for f in frag_list]
for i, fs in enumerate(frag_smiles, 1):
    print(f"  Fragment {i}: {fs}")

Draw.MolsToGridImage(frag_list, legends=[f"Frag #{i+1}" for i in range(len(frag_list))], molsPerRow=3, subImgSize=(280, 200))"""),

        ("markdown", """## 4. Fragment-Based Virtual Design with `BRICSBuild`
Now let's reverse the process: given a pool of retrosynthetic fragments, `BRICS.BRICSBuild` assembles them according to chemical compatibility rules to generate novel candidate molecules!"""),

        ("code", """# Assemble fragments from Imatinib and Aspirin
aspirin = Chem.MolFromSmiles("CC(=O)Oc1ccccc1C(=O)O")
combined_frags = list(Chem.GetMolFrags(BRICS.BreakBRICSBonds(imatinib), asMols=True))
combined_frags.extend(list(Chem.GetMolFrags(BRICS.BreakBRICSBonds(aspirin), asMols=True)))

# Generate novel molecules using BRICS generator
builder = BRICS.BRICSBuild(combined_frags)

novel_molecules = []
for i, mol in enumerate(builder):
    if i >= 6:  # Limit to 6 for speed
        break
    mol.UpdatePropertyCache(strict=False)
    Chem.SanitizeMol(mol)
    novel_molecules.append(mol)

print(f"Generated {len(novel_molecules)} novel virtual molecules!")
Draw.MolsToGridImage(
    novel_molecules,
    legends=[f"Generated #{i+1}\\nMW: {Descriptors.MolWt(m):.1f}" for i, m in enumerate(novel_molecules)],
    molsPerRow=3,
    subImgSize=(300, 200)
)"""),

        ("markdown", """## 5. 🎯 Video Hands-On Challenge & Solution
### Problem:
1. Define a Fischer Esterification reaction SMARTS:
   Carboxylic acid (`[C:1](=O)[O;H1]`) + Alcohol (`[O;H1:2][C:3]`) $\\to$ Ester (`[C:1](=O)[O:2][C:3]`).
2. React Salicylic acid with Methanol to synthesize Methyl salicylate (Oil of Wintergreen).
3. Sanitize and display the product structure."""),

        ("code", """# Fischer Esterification Reaction SMARTS
ester_smarts = "[C:1](=O)[O;H1].[O;H1:2][C:3]>>[C:1](=O)[O:2][C:3]"
ester_rxn = AllChem.ReactionFromSmarts(ester_smarts)

salicylic_acid = Chem.MolFromSmiles("Oc1ccccc1C(=O)O") # Salicylic acid
methanol = Chem.MolFromSmiles("CO")                   # Methanol

ester_products = ester_rxn.RunReactants((salicylic_acid, methanol))
methyl_salicylate = ester_products[0][0]
Chem.SanitizeMol(methyl_salicylate)

print("Esterification Product SMILES:", Chem.MolToSmiles(methyl_salicylate))

Draw.MolsToGridImage(
    [salicylic_acid, methanol, methyl_salicylate],
    legends=["Salicylic Acid", "Methanol", "Methyl Salicylate (Oil of Wintergreen)"],
    molsPerRow=3,
    subImgSize=(300, 220)
)"""),

        ("markdown", """## 6. Summary & Key Takeaways
* **Reaction SMARTS** enables programmatic synthesis of virtual chemical libraries for drug screening.
* **BRICS fragmentation** breaks molecules at synthetically sensible bonds, providing building blocks for fragment-based drug design (FBDD).
* **`BRICSBuild`** assembles fragment libraries into novel, synthetically feasible drug-like candidates.

**Next Up in Video 14:** **3D Conformer Generation & Geometry Optimization** — embedding 3D coordinates, force field minimization (UFF/MMFF94s), and RMSD alignment!""")
    ]
    return create_nb(cells)

# ==============================================================================
# VIDEO 14: 3D Conformer Generation & Geometry Optimization
# ==============================================================================
def build_video_14():
    cells = [
        ("markdown", """# 🎥 Video 14: 3D Conformer Generation & Geometry Optimization
**RDKit Masterclass — From Zero to Drug Discovery AI**
* **Duration:** ~25 - 30 Minutes
* **Curriculum Level:** LEVEL 8 — Advanced RDKit & 3D Conformer Modeling
* **Target Audience:** Computational Chemists, Molecular Docking Scientists, AI Researchers

---

### ⏱️ Video Agenda & Timestamps
* **00:00 - 04:30** | Why 3D Conformations Matter in Drug Binding & Stereochemistry
* **04:30 - 09:30** | Distance Geometry Embedding: `AllChem.EmbedMolecule` & ETKDG v3
* **09:30 - 14:30** | Molecular Mechanics Energy Minimization: UFF vs MMFF94 / MMFF94s
* **14:30 - 19:30** | Conformer Ensemble Generation: `EmbedMultipleConfs` & Energy Ranking
* **19:30 - 24:00** | Calculating RMSD Matrices & Pruning Redundant Conformers
* **24:00 - 27:30** | 3D Pharmacophore Alignment: `AllChem.AlignMol`
* **27:30 - 30:00** | Hands-On Challenge: Exporting Docking-Ready 3D SDF Files

---

### 🎯 Learning Objectives
1. Generate initial 3D coordinates from 1D SMILES using the modern **ETKDG v3** algorithm.
2. Minimize conformational strain energies using the Merck Molecular Force Field (**MMFF94s**).
3. Sample the conformational landscape by generating multi-conformer ensembles.
4. Calculate pairwise Root-Mean-Square Deviations (RMSD) and cluster conformers.
5. Align 3D flexible ligands against a rigid bioactive reference template."""),

        ("code", """# Step 0: Imports and Setup
import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print(f"RDKit Version: {rdkit.__version__}")"""),

        ("markdown", """## 1. Why 3D Conformers?
Small drug molecules are flexible: single bonds rotate freely around dihedral angles.
While SMILES describes 2D graph connectivity, a drug binds to its target receptor in a **specific 3D bioactive conformation** (often within $1-3\\text{ kcal/mol}$ of the global energy minimum).

To generate realistic 3D structures:
1. **Explicit Hydrogens:** Hydrogens must be added (`Chem.AddHs`) so steric clashes and hydrogen-bonding geometries are physically accurate.
2. **Distance Geometry (ETKDG):** Uses experimental torsion-angle knowledge from the Cambridge Structural Database (CSD) to generate initial 3D embeds.
3. **Force Field Minimization:** Optimizes bond lengths, angles, and torsions using MMFF94 or UFF."""),

        ("code", """# Generate 3D coordinates for Ibuprofen
ibuprofen_smi = "CC(C)Cc1ccc(cc1)C(C)C(=O)O"
mol_2d = Chem.MolFromSmiles(ibuprofen_smi)

# 1. Add explicit Hydrogens (CRITICAL for 3D modeling)
mol_3d = Chem.AddHs(mol_2d)
print(f"2D Heavy Atoms: {mol_2d.GetNumAtoms()} -> 3D Total Atoms with Hs: {mol_3d.GetNumAtoms()}")

# 2. Embed 3D coordinates using modern ETKDG v3 parameters
params = AllChem.ETKDGv3()
params.randomSeed = 42
embed_status = AllChem.EmbedMolecule(mol_3d, params)

print(f"Embedding success status (0 = success): {embed_status}")"""),

        ("markdown", """## 2. Molecular Mechanics Energy Minimization (MMFF94s)
The raw distance-geometry embed has geometric strain.
We optimize the geometry using the **Merck Molecular Force Field (MMFF94s)**, designed specifically for drug-like organic molecules and aromatic/heteroaromatic rings."""),

        ("code", """# Energy minimization using MMFF94s
converged = AllChem.MMFFOptimizeMolecule(mol_3d, mmffVariant="MMFF94s", maxIters=1000)
print(f"Force field minimization converged (0 = converged): {converged}")

# Calculate total potential energy
props = AllChem.MMFFGetMoleculeProperties(mol_3d, mmffVariant="MMFF94s")
ff = AllChem.MMFFGetMoleculeForceField(mol_3d, props)
min_energy = ff.CalcEnergy()

print(f"MMFF94s Potential Energy: {min_energy:.2f} kcal/mol")"""),

        ("markdown", """## 3. Conformer Ensemble Generation (`EmbedMultipleConfs`)
Flexible molecules have multiple low-energy conformers.
Let's generate an ensemble of 20 distinct 3D conformers and rank them by relative energy."""),

        ("code", """# Generate 20 conformers for Ibuprofen
embed_params = AllChem.ETKDGv3()
embed_params.pruneRmsThresh = 0.5  # Discard conformers with RMSD < 0.5 Angstrom to avoid duplicates
embed_params.randomSeed = 42

cids = AllChem.EmbedMultipleConfs(mol_3d, 20, embed_params)

print(f"Generated {len(cids)} diverse conformers (after 0.5 Å RMSD pruning).")

# Minimize each conformer and record energies
conformer_energies = []
for cid in cids:
    AllChem.MMFFOptimizeMolecule(mol_3d, confId=cid, mmffVariant="MMFF94s")
    ff = AllChem.MMFFGetMoleculeForceField(mol_3d, props, confId=cid)
    energy = ff.CalcEnergy()
    conformer_energies.append((cid, energy))

# Sort by energy ascending
conformer_energies.sort(key=lambda x: x[1])
lowest_energy = conformer_energies[0][1]

df_confs = pd.DataFrame([
    {"Conf_ID": cid, "Absolute_Energy_kcal_mol": round(e, 2), "Delta_E_kcal_mol": round(e - lowest_energy, 2)}
    for cid, e in conformer_energies
])

print("=== 🔬 TOP 5 LOWEST ENERGY CONFORMERS ===")
display(df_confs.head(5))"""),

        ("markdown", """## 4. Pairwise RMSD Matrix Calculation
We can evaluate how geometrically distinct the conformers are by calculating their pairwise Root-Mean-Square Deviation (RMSD)."""),

        ("code", """# Calculate RMSD matrix relative to the lowest energy conformer (Conf 0)
ref_cid = conformer_energies[0][0]
rms_list = []

for cid, _ in conformer_energies:
    rms = AllChem.GetConformerRMS(mol_3d, ref_cid, cid, prealigned=False)
    rms_list.append(rms)

df_confs["RMSD_to_Best"] = [round(r, 3) for r in rms_list]
display(df_confs.head(5))"""),

        ("markdown", """## 5. 3D Molecular Alignment (`AllChem.AlignMol`)
In pharmacophore modeling, you frequently need to align candidate molecules onto a bioactive reference conformation."""),

        ("code", """# Align conformer 1 onto conformer 0 based on heavy atoms
conf_a = conformer_energies[0][0]
conf_b = conformer_energies[1][0]

rmsd_val = AllChem.AlignMol(mol_3d, mol_3d, prbCid=conf_b, refCid=conf_a)
print(f"Alignment RMSD between Conf {conf_a} and Conf {conf_b}: {rmsd_val:.3f} Å")"""),

        ("markdown", """## 6. 🎯 Video Hands-On Challenge & Solution
### Problem:
1. Export the top 3 lowest-energy 3D conformers of Ibuprofen into an SDF file `ibuprofen_3d_ensemble.sdf`.
2. Attach the relative energy `Delta_E_kcal_mol` as an SD property tag to each conformer.
3. Re-load the SDF and verify that 3 distinct 3D conformers exist."""),

        ("code", """out_3d_sdf = "ibuprofen_3d_ensemble.sdf"
writer = Chem.SDWriter(out_3d_sdf)

for rank, (cid, e) in enumerate(conformer_energies[:3], 1):
    delta_e = e - lowest_energy
    mol_3d.SetProp("_Name", f"Ibuprofen_Conf_{rank}")
    mol_3d.SetDoubleProp("Delta_E_kcal_mol", round(delta_e, 3))
    mol_3d.SetIntProp("Conformer_ID", cid)
    writer.write(mol_3d, confId=cid)

writer.close()

# Verify
suppl_3d = Chem.SDMolSupplier(out_3d_sdf)
print(f"✅ Verified: Loaded {len(suppl_3d)} conformers from '{out_3d_sdf}'")
for m in suppl_3d:
    print(f"  {m.GetProp('_Name')}: Delta_E = {m.GetProp('Delta_E_kcal_mol')} kcal/mol, 3D Conformer count = {m.GetNumConformers()}")"""),

        ("markdown", """## 7. Summary & Key Takeaways
* Always add explicit hydrogens (`Chem.AddHs`) before generating 3D coordinates.
* **ETKDG v3** embeds realistic conformations using experimental torsion rules.
* **MMFF94s** minimizes conformational strain energies for drug-like molecules.
* Conformer ensembles with RMSD pruning capture the flexible 3D shape space for molecular docking and pharmacophore modeling.

**Next Up in Video 15:** **Machine Learning QSAR & Modern AI Representations** — scaffold-based splitting, predicting bioactivity ($pIC_{50}$), and transitioning to molecular graphs!""")
    ]
    return create_nb(cells)

# ==============================================================================
# VIDEO 15: Machine Learning QSAR & Modern AI Representations
# ==============================================================================
def build_video_15():
    cells = [
        ("markdown", """# 🎥 Video 15: Machine Learning QSAR & Modern AI Representations
**RDKit Masterclass — From Zero to Drug Discovery AI**
* **Duration:** ~25 - 30 Minutes
* **Curriculum Level:** LEVEL 7 (Topics 36-40) & LEVEL 10 (Topics 54-59)
* **Target Audience:** AI/ML Engineers, Cheminformatics Scientists, Computational Biologists

---

### ⏱️ Video Agenda & Timestamps
* **00:00 - 05:00** | QSAR Principles & Why Random Train/Test Splits Fail in Chemistry
* **05:00 - 10:00** | Scaffold-Based Splitting (Bemis-Murcko) to Prevent Data Leakage
* **10:00 - 15:00** | Hybrid Featurization: Morgan ECFP4 + RDKit 2D Physicochemical Descriptors
* **15:00 - 20:00** | Training & Evaluating Random Forest Regressors for Bioactivity ($pIC_{50}$)
* **20:00 - 24:00** | Model Interpretability: Feature Importance & Potency Drivers
* **24:00 - 27:30** | Transition to Modern Deep Learning: Representing Molecules as Graphs (PyG Format)
* **27:30 - 30:00** | Hands-On Challenge & Summary

---

### 🎯 Learning Objectives
1. Understand **Quantitative Structure-Activity Relationships (QSAR)**.
2. Implement **Bemis-Murcko Scaffold Splitting** to ensure models generalize to novel chemical scaffolds.
3. Train, validate, and evaluate Machine Learning regressors ($R^2$, RMSE, MAE) on real ChEMBL bioactivity data.
4. Extract feature importances to determine which chemical features govern target inhibition.
5. Convert RDKit `Mol` objects into **Molecular Graph Data structures** (Nodes = Atom features, Edges = Bond adjacency) for PyTorch Geometric GNNs."""),

        ("code", """# Step 0: Imports and Setup
import os
import rdkit
from rdkit import Chem
from rdkit.Chem import Descriptors, rdFingerprintGenerator
from rdkit.Chem.Scaffolds import MurckoScaffold
from rdkit import DataStructs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

print(f"RDKit Version: {rdkit.__version__}")"""),

        ("markdown", """## 1. Why Random Splitting Fails in Drug Discovery
In standard machine learning (e.g. image or text classification), random $80/20$ train/test splitting is routine.
In cheminformatics, **random splitting creates massive data leakage**!
Why? If an analog series of 15 compounds with the exact same core scaffold is split randomly, the model memorizes the scaffold in training and easily predicts the test compounds. When tested on a **completely new scaffold** in prospective wet-lab experiments, accuracy collapses!

**The Solution: Scaffold Splitting (Bemis-Murcko)**
Group compounds by their Murcko scaffold so that all molecules with the same scaffold reside in either the train OR test set, never both!"""),

        ("code", """# Load ChEMBL EGFR bioactivity dataset
candidate_paths = [
    "datasets/EGFR_compounds.csv",
    "../datasets/EGFR_compounds.csv",
    "../../datasets/EGFR_compounds.csv",
    os.path.expanduser("~/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/datasets/EGFR_compounds.csv")
]
csv_path = next((p for p in candidate_paths if os.path.exists(p)), None)

df_raw = pd.read_csv(csv_path).dropna(subset=["smiles", "pIC50"]).head(500)
print(f"Loaded {len(df_raw)} EGFR bioactivity records.")"""),

        ("markdown", """## 2. Implementing Bemis-Murcko Scaffold Splitting"""),

        ("code", """def scaffold_split(df, smiles_col="smiles", test_size=0.2):
    \"\"\"Splits a DataFrame into train and test sets based on Bemis-Murcko scaffolds.\"\"\"
    scaffold_dict = {}
    
    for idx, smi in enumerate(df[smiles_col]):
        m = Chem.MolFromSmiles(smi)
        if m:
            scaff = MurckoScaffold.GetScaffoldForMol(m)
            scaff_smi = Chem.MolToSmiles(scaff)
            if scaff_smi not in scaffold_dict:
                scaffold_dict[scaff_smi] = []
            scaffold_dict[scaff_smi].append(idx)
            
    # Sort scaffold groups from largest to smallest
    sorted_scaffolds = sorted(scaffold_dict.values(), key=len, reverse=True)
    
    train_indices = []
    test_indices = []
    total_samples = len(df)
    target_test_count = int(total_samples * test_size)
    
    for group in sorted_scaffolds:
        if len(test_indices) + len(group) <= target_test_count:
            test_indices.extend(group)
        else:
            train_indices.extend(group)
            
    return train_indices, test_indices

train_idx, test_idx = scaffold_split(df_raw)
print(f"Train set: {len(train_idx)} compounds ({len(train_idx)/len(df_raw):.1%})")
print(f"Test set:  {len(test_idx)} compounds ({len(test_idx)/len(df_raw):.1%})")"""),

        ("markdown", """## 3. Hybrid Molecular Featurization
We featurize our molecules using a hybrid combination:
1. **1024-bit Morgan Fingerprints (ECFP4)**
2. **6 Physicochemical Descriptors** (MW, LogP, TPSA, HBD, HBA, RotBonds)"""),

        ("code", """mfpgen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=1024)

def featurize_molecule(mol):
    # Fingerprint
    fp = mfpgen.GetFingerprint(mol)
    fp_arr = np.zeros((1024,), dtype=np.float32)
    DataStructs.ConvertToNumpyArray(fp, fp_arr)
    
    # Descriptors
    desc_arr = np.array([
        Descriptors.MolWt(mol) / 500.0,
        Descriptors.MolLogP(mol) / 5.0,
        Descriptors.TPSA(mol) / 140.0,
        Descriptors.NumHDonors(mol) / 5.0,
        Descriptors.NumHAcceptors(mol) / 10.0,
        Descriptors.NumRotatableBonds(mol) / 10.0
    ], dtype=np.float32)
    
    return np.concatenate([fp_arr, desc_arr])

# Featurize dataset
X_all = np.array([featurize_molecule(Chem.MolFromSmiles(s)) for s in df_raw["smiles"]])
y_all = df_raw["pIC50"].values

X_train, y_train = X_all[train_idx], y_all[train_idx]
X_test, y_test = X_all[test_idx], y_all[test_idx]

print(f"Feature matrix shape: {X_train.shape}")"""),

        ("markdown", """## 4. Training & Evaluating Random Forest QSAR Regressor"""),

        ("code", """rf_model = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)

# Predictions
y_pred_train = rf_model.predict(X_train)
y_pred_test = rf_model.predict(X_test)

# Metrics
r2_tr = r2_score(y_train, y_pred_train)
r2_te = r2_score(y_test, y_pred_test)
rmse_te = np.sqrt(mean_squared_error(y_test, y_pred_test))
mae_te = mean_absolute_error(y_test, y_pred_test)

print("=== 📊 QSAR MODEL EVALUATION ===")
print(f"  Train R²: {r2_tr:.3f}")
print(f"  Test R²:  {r2_te:.3f}  (Rigorous out-of-scaffold test set!)")
print(f"  Test RMSE: {rmse_te:.3f}")
print(f"  Test MAE:  {mae_te:.3f}")"""),

        ("markdown", """## 5. Visualizing Actual vs Predicted $pIC_{50}$"""),

        ("code", """plt.figure(figsize=(7, 7))
plt.scatter(y_test, y_pred_test, alpha=0.7, color="#2b5c8f", edgecolor="black", s=50)
min_val = min(y_test.min(), y_pred_test.min()) - 0.5
max_val = max(y_test.max(), y_pred_test.max()) + 0.5

plt.plot([min_val, max_val], [min_val, max_val], "r--", linewidth=2, label="Ideal Line (y = x)")
plt.xlabel("Actual Experimental pIC50", fontsize=12)
plt.ylabel("Predicted pIC50", fontsize=12)
plt.title(f"Random Forest QSAR Bioactivity Prediction\\nTest R² = {r2_te:.2f}, RMSE = {rmse_te:.2f}", fontsize=13)
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()"""),

        ("markdown", """## 6. Transition to Modern AI: Molecules as Graphs (PyTorch Geometric)
Traditional QSAR uses flat vectors (fingerprints).
Modern AI treats molecules as **Chemical Graphs**:
* **Nodes ($V$):** Atoms. Feature vector per atom (atomic number, formal charge, hybridization, aromaticity).
* **Edges ($E$):** Chemical bonds. Adjacency list and bond types.

Let's write an RDKit converter that constructs a PyG-compatible Graph Data dictionary!"""),

        ("code", """def mol_to_graph_dict(mol):
    \"\"\"Converts an RDKit Mol object into a graph representation for PyTorch Geometric.\"\"\"
    # 1. Node features (Atom attributes)
    atom_features = []
    for atom in mol.GetAtoms():
        feature_vector = [
            atom.GetAtomicNum(),
            atom.GetFormalCharge(),
            atom.GetTotalNumHs(),
            int(atom.GetIsAromatic()),
            int(atom.GetHybridization())
        ]
        atom_features.append(feature_vector)
        
    x = np.array(atom_features, dtype=np.float32)
    
    # 2. Edge Index (Bond connectivity [2, 2*num_bonds])
    edge_indices = []
    edge_types = []
    for bond in mol.GetBonds():
        i = bond.GetBeginAtomIdx()
        j = bond.GetEndAtomIdx()
        b_type = float(bond.GetBondTypeAsDouble())
        
        # Undirected graph -> add both directions (i->j and j->i)
        edge_indices.extend([[i, j], [j, i]])
        edge_types.extend([b_type, b_type])
        
    edge_index = np.array(edge_indices, dtype=np.int64).T
    edge_attr = np.array(edge_types, dtype=np.float32)
    
    return {
        "num_nodes": mol.GetNumAtoms(),
        "x": x,
        "edge_index": edge_index,
        "edge_attr": edge_attr
    }

# Convert Aspirin to Graph representation
aspirin = Chem.MolFromSmiles("CC(=O)Oc1ccccc1C(=O)O")
graph_data = mol_to_graph_dict(aspirin)

print("=== 🧠 GRAPH REPRESENTATION: ASPIRIN ===")
print("Number of Nodes (Atoms):", graph_data["num_nodes"])
print("Node Feature Matrix x shape:", graph_data["x"].shape)
print("Edge Index shape (2 x 2*Bonds):", graph_data["edge_index"].shape)
print("Sample Node Features (First 3 atoms):\\n", graph_data["x"][:3])"""),

        ("markdown", """## 7. 🎯 Video Hands-On Challenge & Solution
### Problem:
Take the trained Random Forest model and run **prospective screening** on 3 approved drugs:
* **Gefitinib** (Known potent EGFR inhibitor)
* **Aspirin** (Unrelated NSAID)
* **Paracetamol** (Unrelated analgesic)
1. Featurize each molecule using `featurize_molecule`.
2. Predict their $pIC_{50}$ values.
3. Compare the predictions to chemical expectations!"""),

        ("code", """test_compounds = {
    "Gefitinib (Known EGFR Drug)": Chem.MolFromSmiles("COc1cc2ncnc(Nc3ccc(F)c(Cl)c3)c2cc1OCCCN4CCOCC4"),
    "Aspirin (NSAID)": Chem.MolFromSmiles("CC(=O)Oc1ccccc1C(=O)O"),
    "Paracetamol (Analgesic)": Chem.MolFromSmiles("CC(=O)Nc1ccc(O)cc1")
}

for name, m in test_compounds.items():
    feats = featurize_molecule(m).reshape(1, -1)
    pred_pic50 = rf_model.predict(feats)[0]
    # Convert pIC50 to estimated IC50 (nM)
    ic50_nm = 10 ** (9 - pred_pic50)
    print(f"Compound: {name:<30} | Pred pIC50: {pred_pic50:.2f} | Est. IC50: {ic50_nm:.1f} nM")"""),

        ("markdown", """## 8. Summary & Key Takeaways
* **Scaffold Splitting** is mandatory in life sciences AI to evaluate real-world generalizability.
* **Hybrid Featurization** (Fingerprints + 2D Descriptors) captures both fine structural patterns and global bulk properties.
* **Molecular Graphs** represent the cutting edge of AI, directly mapping atomic nodes and chemical bonds into Graph Neural Networks (GNNs).

**Next Up:** **Capstone Projects 01 & 02** — building complete, production-grade end-to-end drug discovery pipelines!""")
    ]
    return create_nb(cells)

# ==============================================================================
# MAIN RUNNER FOR VIDEOS 11 TO 15
# ==============================================================================
if __name__ == "__main__":
    base_dir = "/home/softvence/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/RDKit Tutorials"
    
    video_configs = [
        ("10_Scaffold_Analysis/Video_11_Chemical_Space_Visualization_and_Clustering.ipynb", build_video_11),
        ("10_Scaffold_Analysis/Video_12_Scaffold_Analysis_and_Molecular_Decomposition.ipynb", build_video_12),
        ("12_Chemical_Reaction_Processing/Video_13_Chemical_Reactions_and_BRICS_Fragmentation.ipynb", build_video_13),
        ("11_3D_Conformer_Generation/Video_14_3D_Conformers_and_Geometry_Optimization.ipynb", build_video_14),
        ("14_QSAR_Machine_Learning/Video_15_Machine_Learning_QSAR_and_Modern_AI.ipynb", build_video_15)
    ]
    
    for rel_path, builder_func in video_configs:
        full_path = os.path.join(base_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        nb = builder_func()
        with open(full_path, "w", encoding="utf-8") as f:
            nbf.write(nb, f)
        print(f"Generated: {rel_path} ({len(nb.cells)} cells)")
