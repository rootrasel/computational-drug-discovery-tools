#!/usr/bin/env python3
"""
Generator script for Video Tutorials 06 to 10 of the RDKit Master Playlist.
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
# VIDEO 06: Drug-Likeness Rules & MedChem Filters
# ==============================================================================
def build_video_06():
    cells = [
        ("markdown", """# 🎥 Video 06: Drug-Likeness Rules & MedChem Filters
**RDKit Masterclass — From Zero to Drug Discovery AI**
* **Duration:** ~25 - 30 Minutes
* **Curriculum Level:** LEVEL 2 (Topic 09: Lipinski's Rule of 5) & LEVEL 4 (Topic 23: MedChem Filters)
* **Target Audience:** Cheminformatics Engineers, Medicinal Chemists, Screening Scientists

---

### ⏱️ Video Agenda & Timestamps
* **00:00 - 04:30** | Oral Bioavailability & The Chemistry of Drug-Likeness
* **04:30 - 09:30** | Lipinski's Rule of Five (Ro5) & Pfizer 3/75 Rule
* **09:30 - 14:00** | Veber's Rules, Ghose Filter & Lead-Likeness / Rule of Three (Ro3)
* **14:00 - 19:30** | Filtering Toxicophores: PAINS & Brenk Alerts via `FilterCatalog`
* **19:30 - 24:30** | Building an Interactive Drug-Likeness Scorecard & Radar Chart
* **24:30 - 28:00** | Screening a Real Library for Development Candidates
* **28:00 - 30:00** | Hands-On Challenge & Summary

---

### 🎯 Learning Objectives
1. Implement Lipinski's Rule of Five and count violations programmatically.
2. Apply Veber's bioavailability rules (RotBonds $\\le 10$, $\\text{TPSA} \\le 140\\text{ Å}^2$).
3. Screen compounds against PAINS (Pan-Assay Interference Compounds) using RDKit's `FilterCatalog`.
4. Screen for reactive/unwanted functional groups with Brenk structural alerts.
5. Create a multi-dimensional drug-likeness radar chart comparing candidate molecules."""),

        ("code", """# Step 0: Imports and Environment Setup
import os
import rdkit
from rdkit import Chem
from rdkit.Chem import Descriptors, Draw, rdMolDescriptors
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"RDKit Version: {rdkit.__version__}")"""),

        ("markdown", """## 1. Lipinski's Rule of Five (Ro5)
Formulated by Christopher Lipinski (Pfizer) in 1997, the Rule of 5 predicts whether a chemical compound has structural and physicochemical properties compatible with good **oral bioavailability**:
* **Molecular Weight (MW)** $\\le 500\\text{ Da}$
* **LogP (Lipophilicity)** $\\le 5.0$
* **Hydrogen Bond Donors (HBD)** $\\le 5$ (sum of OH and NH groups)
* **Hydrogen Bond Acceptors (HBA)** $\\le 10$ (sum of Oxygen and Nitrogen atoms)

*Note:* A molecule is considered **Lipinski compliant** if it has **$\\le 1$ violation**."""),

        ("code", """def calculate_lipinski(mol):
    \"\"\"Calculates Lipinski properties and violation count for a Mol object.\"\"\"
    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    hbd = Descriptors.NumHDonors(mol)
    hba = Descriptors.NumHAcceptors(mol)
    
    violations = 0
    if mw > 500: violations += 1
    if logp > 5.0: violations += 1
    if hbd > 5: violations += 1
    if hba > 10: violations += 1
    
    return {
        "MW": round(mw, 2),
        "LogP": round(logp, 2),
        "HBD": hbd,
        "HBA": hba,
        "Ro5_Violations": violations,
        "Ro5_Pass": violations <= 1
    }

# Test on Aspirin and Atorvastatin (Lipitor)
aspirin = Chem.MolFromSmiles("CC(=O)Oc1ccccc1C(=O)O")
atorvastatin = Chem.MolFromSmiles("CC(C)c1c(C(=O)Nc2ccccc2)c(c3ccc(F)cc3)c(c4ccccc4)n1CCC(O)CC(O)CC(=O)O")

print("Aspirin Lipinski Profile:     ", calculate_lipinski(aspirin))
print("Atorvastatin Lipinski Profile:", calculate_lipinski(atorvastatin))"""),

        ("markdown", """## 2. Veber's Rules & Oral Bioavailability
In 2002, Daniel Veber (GSK) demonstrated that molecular flexibility and polar surface area are even better predictors of oral bioavailability in rats:
* **Rotatable Bonds** $\\le 10$ (Rigidity enhances cellular permeation)
* **Topological Polar Surface Area (TPSA)** $\\le 140\\text{ Å}^2$ (or sum of H-bond donors & acceptors $\\le 12$)"""),

        ("code", """def check_veber_rules(mol):
    rot_bonds = Descriptors.NumRotatableBonds(mol)
    tpsa = Descriptors.TPSA(mol)
    passes = (rot_bonds <= 10) and (tpsa <= 140.0)
    return {
        "RotatableBonds": rot_bonds,
        "TPSA": round(tpsa, 2),
        "Veber_Pass": passes
    }

print("Aspirin Veber:     ", check_veber_rules(aspirin))
print("Atorvastatin Veber:", check_veber_rules(atorvastatin))"""),

        ("markdown", """## 3. Structural Alerts: PAINS & Brenk Filters (`FilterCatalog`)
**PAINS (Pan-Assay Interference Compounds):** Compounds that show false-positive activity in biochemical high-throughput screening (HTS) through covalent modification, redox cycling, fluorescence interference, or colloidal aggregation (e.g. Rhodanines, Catechols, Quinones).
**Brenk Alerts:** Structural alerts for chemically reactive, unstable, or mutagenic groups (e.g. Epoxides, Alkyl halides, Nitroso groups)."""),

        ("code", """# Initialize FilterCatalog with PAINS and BRENK rules
params = FilterCatalogParams()
params.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS)
params.AddCatalog(FilterCatalogParams.FilterCatalogs.BRENK)
catalog = FilterCatalog(params)

# Test molecules: A clean drug vs a known PAINS compound (Rhodanine derivative)
test_compounds = [
    ("Aspirin (Clean)", "CC(=O)Oc1ccccc1C(=O)O"),
    ("Gefitinib (Clean)", "COc1cc2ncnc(Nc3ccc(F)c(Cl)c3)c2cc1OCCCN4CCOCC4"),
    ("Rhodanine PAINS (Interfering)", "O=C1NC(=S)S/C1=C/c2ccc(O)cc2"),
    ("Alkyl Halide (Reactive Brenk)", "CCNCCCl")
]

for name, smi in test_compounds:
    m = Chem.MolFromSmiles(smi)
    matches = catalog.GetMatches(m)
    if matches:
        descriptions = [entry.GetDescription() for entry in matches]
        print(f"🚨 ALERT on '{name}': {descriptions}")
    else:
        print(f"✅ CLEAN '{name}': No structural alerts found.")"""),

        ("markdown", """## 4. Multi-Parameter Drug-Likeness Scorecard & Radar Chart
Let's build a visual radar/spider chart comparing candidate molecules across 6 standardized drug-likeness dimensions (MW, LogP, TPSA, HBD, HBA, Rotatable Bonds)."""),

        ("code", """def plot_drug_likeness_radar(molecules_dict):
    categories = ['MW/500', 'LogP/5', 'TPSA/140', 'HBD/5', 'HBA/10', 'RotB/10']
    N = len(categories)
    
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    plt.xticks(angles[:-1], categories, color='grey', size=11)
    
    # Draw reference boundary for ideal drug-likeness (value <= 1.0)
    ideal = [1.0] * N
    ideal += ideal[:1]
    ax.plot(angles, ideal, color='red', linestyle='--', linewidth=1.5, label='Drug-Like Threshold (1.0)')
    ax.fill(angles, ideal, color='red', alpha=0.05)
    
    for name, mol in molecules_dict.items():
        mw = Descriptors.MolWt(mol) / 500.0
        logp = max(0, Descriptors.MolLogP(mol)) / 5.0
        tpsa = Descriptors.TPSA(mol) / 140.0
        hbd = Descriptors.NumHDonors(mol) / 5.0
        hba = Descriptors.NumHAcceptors(mol) / 10.0
        rot = Descriptors.NumRotatableBonds(mol) / 10.0
        
        values = [mw, logp, tpsa, hbd, hba, rot]
        values += values[:1]
        
        ax.plot(angles, values, linewidth=2, label=name)
        ax.fill(angles, values, alpha=0.15)
        
    plt.title("Drug-Likeness Multi-Parameter Radar Comparison", size=14, y=1.08)
    plt.legend(loc='upper right', bbox_to_anchor=(1.25, 1.1))
    plt.show()

# Compare Aspirin vs Atorvastatin
plot_drug_likeness_radar({
    "Aspirin": aspirin,
    "Atorvastatin": atorvastatin
})"""),

        ("markdown", """## 5. 🎯 Video Hands-On Challenge & Solution
### Problem:
Given a small virtual library of 4 candidate compounds:
1. Check Lipinski compliance (violations $\\le 1$).
2. Check Veber compliance.
3. Check PAINS / Brenk structural alerts.
4. Output a summary decision table: `"PASS"` or `"REJECT"`.
5. Display passing molecules in a grid."""),

        ("code", """library = {
    "Candidate_A": "Cc1ccc(cc1)C(=O)Nc2ccc(cc2)C(=O)O",
    "Candidate_B": "O=C1NC(=S)SC1=Cc2ccc(O)c(O)c2",       # PAINS Rhodanine + Catechol
    "Candidate_C": "COc1cc2ncnc(Nc3cccc(c3)Cl)c2cc1OC",   # Kinase inhibitor core
    "Candidate_D": "CCCCCCCCCCCCCCC(=O)O"                 # Palmitic acid (high LogP/RotB)
}

screening_results = []
passing_mols = []
passing_legends = []

for name, smi in library.items():
    mol = Chem.MolFromSmiles(smi)
    lip = calculate_lipinski(mol)
    veb = check_veber_rules(mol)
    has_alert = len(catalog.GetMatches(mol)) > 0
    
    passes = lip["Ro5_Pass"] and veb["Veber_Pass"] and (not has_alert)
    status = "PASS" if passes else "REJECT"
    
    screening_results.append({
        "Compound": name,
        "MW": lip["MW"],
        "LogP": lip["LogP"],
        "Ro5_Violations": lip["Ro5_Violations"],
        "Veber_Pass": veb["Veber_Pass"],
        "Alert_Found": has_alert,
        "Status": status
    })
    
    if passes:
        passing_mols.append(mol)
        passing_legends.append(f"{name} (PASSED)")

df_screen = pd.DataFrame(screening_results)
print("=== 🧪 VIRTUAL SCREENING SCORECARD ===")
display(df_screen)

if passing_mols:
    Draw.MolsToGridImage(passing_mols, legends=passing_legends, molsPerRow=2, subImgSize=(300, 200))"""),

        ("markdown", """## 6. Summary & Key Takeaways
* **Lipinski Rule of 5:** Guides oral druggability based on size, lipophilicity, and H-bonding.
* **Veber's Rules:** Focuses on flexibility (rotatable bonds $\\le 10$) and polarity (TPSA $\\le 140\\text{ Å}^2$).
* **`FilterCatalog`:** Automated detection of PAINS false positives and Brenk reactive groups.
* In early virtual screening, combining Lipinski + Veber + PAINS filters weeds out $70\\%+ $ of untreatable or misleading hits.

**Next Up in Video 07:** **Molecular Fingerprints Deep Dive** — Morgan / ECFP, MACCS keys, and converting structures into machine-learning bit vectors!""")
    ]
    return create_nb(cells)

# ==============================================================================
# VIDEO 07: Molecular Fingerprints Deep Dive
# ==============================================================================
def build_video_07():
    cells = [
        ("markdown", """# 🎥 Video 07: Molecular Fingerprints Deep Dive
**RDKit Masterclass — From Zero to Drug Discovery AI**
* **Duration:** ~25 - 30 Minutes
* **Curriculum Level:** LEVEL 3 — Molecular Fingerprints (Topics 13, 14, 15, 16, 17)
* **Target Audience:** AI/ML Engineers, Cheminformatics Researchers, Data Scientists

---

### ⏱️ Video Agenda & Timestamps
* **00:00 - 05:00** | Descriptors vs Fingerprints: Molecular Properties vs Structural Bit Patterns
* **05:00 - 10:00** | Circular Fingerprints: The Morgan / ECFP Algorithm Explained
* **10:00 - 14:30** | ECFP4 vs ECFP6: Radius, Bit Size, Hashing & Bit Collisions
* **14:30 - 18:30** | Modern RDKit API: `rdFingerprintGenerator.GetMorganGenerator`
* **18:30 - 22:30** | Structural Keys: MACCS Keys (166 predefined bits)
* **22:30 - 26:30** | Topological Fingerprints: RDKit Daylight-like & Atom Pairs
* **26:30 - 30:00** | Converting to NumPy Arrays for Scikit-Learn & PyTorch

---

### 🎯 Learning Objectives
1. Understand why fixed-length bit vectors are necessary for chemical machine learning.
2. Master circular Extended Connectivity Fingerprints (ECFP) and choose between radius 2 (ECFP4) and radius 3 (ECFP6).
3. Use the modern `rdFingerprintGenerator` architecture introduced in recent RDKit releases.
4. Calculate structural key fingerprints (MACCS 166 keys) and compare with Morgan fingerprints.
5. Convert RDKit bit vectors into dense NumPy arrays for machine learning pipelines."""),

        ("code", """# Step 0: Imports and Setup
import rdkit
from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator, MACCSkeys, RDKFingerprint
from rdkit import DataStructs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print(f"RDKit Version: {rdkit.__version__}")"""),

        ("markdown", """## 1. Descriptors vs Molecular Fingerprints
* **Physicochemical Descriptors (e.g. MW, LogP, TPSA):** Aggregate global properties. Two completely different structures (e.g. a long aliphatic chain vs an aromatic ring) can have identical MW and LogP.
* **Molecular Fingerprints:** Encode the presence or absence of specific **substructural fragment patterns** as binary bits ($0$ or $1$) in a high-dimensional vector space (e.g. 1024 or 2048 bits).

Fingerprints enable:
1. Fast chemical similarity search.
2. Molecular clustering and diversity analysis.
3. Feature vectors for Machine Learning classifiers and regressors."""),

        ("code", """# Let's inspect Aspirin and Paracetamol
aspirin = Chem.MolFromSmiles("CC(=O)Oc1ccccc1C(=O)O")
paracetamol = Chem.MolFromSmiles("CC(=O)Nc1ccc(O)cc1")

print(f"Aspirin heavy atoms:     {aspirin.GetNumAtoms()}")
print(f"Paracetamol heavy atoms: {paracetamol.GetNumAtoms()}")"""),

        ("markdown", """## 2. Morgan / ECFP Fingerprints Explained
The **Extended Connectivity Fingerprint (ECFP)** algorithm:
1. Assigns initial integer identifiers to each atom based on atomic number, charge, valence, etc.
2. Iteratively updates each atom's identifier by hashing the identifiers of its immediate neighbors in concentric spheres of radius $r$.
3. At iteration $r=1$: captures immediate atom pairs (radius 1, diameter 2 -> ECFP2).
4. At iteration $r=2$: captures 2-bond neighborhoods (radius 2, diameter 4 -> **ECFP4**).
5. Hashes the resulting integer IDs into a fixed-length bit vector (e.g. 1024 or 2048 bits) using modulo arithmetic."""),

        ("code", """# Modern RDKit API: rdFingerprintGenerator
# ECFP4 (Radius = 2, Length = 2048)
morgan_gen_r2 = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
fp_aspirin_r2 = morgan_gen_r2.GetFingerprint(aspirin)

# ECFP6 (Radius = 3, Length = 2048)
morgan_gen_r3 = rdFingerprintGenerator.GetMorganGenerator(radius=3, fpSize=2048)
fp_aspirin_r3 = morgan_gen_r3.GetFingerprint(aspirin)

print(f"ECFP4 (radius 2) active 'on' bits: {fp_aspirin_r2.GetNumOnBits()} / 2048")
print(f"ECFP6 (radius 3) active 'on' bits: {fp_aspirin_r3.GetNumOnBits()} / 2048")"""),

        ("markdown", """## 3. Count Vectors vs Bit Vectors
A standard **Bit Vector** only records whether a fragment is present ($0$ or $1$).
A **Count Vector** records how many times that exact fragment appears (e.g. 3 methyl groups = count 3), preserving stoichiometry."""),

        ("code", """# Generate Count Fingerprint
fp_count = morgan_gen_r2.GetCountFingerprint(aspirin)
non_zero_elements = fp_count.GetNonzeroElements()
print(f"Number of unique fragment environments: {len(non_zero_elements)}")
print("Sample (bit_id: count):", dict(list(non_zero_elements.items())[:5]))"""),

        ("markdown", """## 4. MACCS Keys (166 Predefined Structural Patterns)
**MACCS (Molecular ACCess System) Keys** are 166 predefined SMARTS patterns (e.g., bit 125 = aromatic ring, bit 84 = halogen, bit 155 = OH group).
Unlike Morgan fingerprints, there are **no hash collisions** in MACCS keys, and every bit has a fixed, documented chemical meaning!"""),

        ("code", """maccs_aspirin = MACCSkeys.GenMACCSKeys(aspirin)
maccs_paracetamol = MACCSkeys.GenMACCSKeys(paracetamol)

print(f"MACCS Keys Total Bits: {maccs_aspirin.GetNumBits()}")
print(f"Aspirin 'on' bits:     {maccs_aspirin.GetNumOnBits()}")
print(f"Paracetamol 'on' bits: {maccs_paracetamol.GetNumOnBits()}")"""),

        ("markdown", """## 5. Topological & Atom-Pair Fingerprints
* **RDKit Topological (Daylight-like):** Hashes linear paths of atoms and bonds up to a default length of 7.
* **Atom Pair Fingerprints:** Encodes pairs of atoms and the shortest topological path distance between them (e.g., `C_sp3` separated by 4 bonds from `O_sp2`)."""),

        ("code", """# RDKit Topological Fingerprint
rdk_gen = rdFingerprintGenerator.GetRDKitFPGenerator(minPath=1, maxPath=7, fpSize=2048)
fp_rdk = rdk_gen.GetFingerprint(aspirin)

# Atom Pair Fingerprint
atom_pair_gen = rdFingerprintGenerator.GetAtomPairGenerator(minDistance=1, maxDistance=30, fpSize=2048)
fp_atompair = atom_pair_gen.GetFingerprint(aspirin)

print(f"RDKit Topological 'on' bits: {fp_rdk.GetNumOnBits()}")
print(f"Atom Pair 'on' bits:         {fp_atompair.GetNumOnBits()}")"""),

        ("markdown", """## 6. Converting RDKit Fingerprints to NumPy Arrays
For integration with **Scikit-Learn**, **XGBoost**, or **PyTorch**, you need dense or sparse NumPy arrays."""),

        ("code", """def fp_to_numpy(rdkit_fp):
    \"\"\"Converts an ExplicitBitVect into a 1D numpy array of float32.\"\"\"
    arr = np.zeros((rdkit_fp.GetNumBits(),), dtype=np.float32)
    DataStructs.ConvertToNumpyArray(rdkit_fp, arr)
    return arr

arr_aspirin = fp_to_numpy(fp_aspirin_r2)
print(f"NumPy array shape: {arr_aspirin.shape}")
print(f"NumPy array dtype: {arr_aspirin.dtype}")
print(f"First 25 bits:     {arr_aspirin[:25].astype(int)}")"""),

        ("markdown", """## 7. 🎯 Video Hands-On Challenge & Solution
### Problem:
Take 3 structurally distinct drugs:
* **Gefitinib** (Kinase inhibitor, multi-ring aromatic)
* **Penicillin V** (Beta-lactam antibiotic)
* **Ibuprofen** (Small NSAID)
1. Generate ECFP4 (Morgan r=2), MACCS keys, and RDKit Topological fingerprints for each.
2. Calculate the bit density (`on_bits / total_bits`) for each fingerprint type.
3. Compare their bit overlap."""),

        ("code", """challenge_drugs = {
    "Gefitinib": "COc1cc2ncnc(Nc3ccc(F)c(Cl)c3)c2cc1OCCCN4CCOCC4",
    "Penicillin V": "CC1(C(N2C(S1)C(C2=O)NC(=O)COc3ccccc3)C(=O)O)C",
    "Ibuprofen": "CC(C)Cc1ccc(cc1)C(C)C(=O)O"
}

summary = []
for name, smi in challenge_drugs.items():
    m = Chem.MolFromSmiles(smi)
    fp_ecfp4 = morgan_gen_r2.GetFingerprint(m)
    fp_maccs = MACCSkeys.GenMACCSKeys(m)
    fp_rdk = rdk_gen.GetFingerprint(m)
    
    summary.append({
        "Drug": name,
        "HeavyAtoms": m.GetNumAtoms(),
        "ECFP4_OnBits": fp_ecfp4.GetNumOnBits(),
        "ECFP4_Density": f"{fp_ecfp4.GetNumOnBits() / 2048:.2%}",
        "MACCS_OnBits": fp_maccs.GetNumOnBits(),
        "MACCS_Density": f"{fp_maccs.GetNumOnBits() / 166:.2%}",
        "RDKit_OnBits": fp_rdk.GetNumOnBits(),
        "RDKit_Density": f"{fp_rdk.GetNumOnBits() / 2048:.2%}"
    })

df_fp = pd.DataFrame(summary)
print("=== 🔬 FINGERPRINT COMPARISON TABLE ===")
display(df_fp)"""),

        ("markdown", """## 8. Summary & Key Takeaways
* **Morgan / ECFP4** is the gold standard fingerprint for molecular property prediction, QSAR, and similarity searching.
* **`rdFingerprintGenerator.GetMorganGenerator()`** is the modern thread-safe API replacing legacy functions.
* **MACCS Keys** provide fixed, interpretable structural features (166 bits) without bit collisions.
* `DataStructs.ConvertToNumpyArray()` bridges the gap between RDKit and Python Machine Learning ecosystems.

**Next Up in Video 08:** **Molecular Similarity & Similarity Searching** — calculating Tanimoto, Dice, Cosine similarities, and building a high-speed chemical search engine!""")
    ]
    return create_nb(cells)

# ==============================================================================
# VIDEO 08: Molecular Similarity & Similarity Searching
# ==============================================================================
def build_video_08():
    cells = [
        ("markdown", """# 🎥 Video 08: Molecular Similarity & Similarity Searching
**RDKit Masterclass — From Zero to Drug Discovery AI**
* **Duration:** ~25 - 30 Minutes
* **Curriculum Level:** LEVEL 3 — Molecular Fingerprints (Topics 18 & 19)
* **Target Audience:** Cheminformatics Engineers, Screening Scientists, Computational Chemists

---

### ⏱️ Video Agenda & Timestamps
* **00:00 - 04:30** | The Similar Property Principle: Why Molecular Similarity Matters
* **04:30 - 09:30** | Mathematical Similarity Metrics: Tanimoto (Jaccard), Dice, Cosine, Tversky
* **09:30 - 14:00** | Pairwise Similarity Matrices & Distance Computation
* **14:00 - 19:30** | High-Speed Library Screening with `DataStructs.BulkTanimotoSimilarity`
* **19:30 - 24:30** | Building a "Find Similar Drugs" Search Engine (Top-K Ranking)
* **24:30 - 27:30** | Atom-Level Similarity Attribution: Riniker & Landrum Similarity Maps
* **27:30 - 30:00** | Hands-On Challenge & Summary

---

### 🎯 Learning Objectives
1. Understand Johnson & Maggiora's **Similar Property Principle**: Structurally similar molecules exhibit similar biological activities.
2. Master mathematical definitions: Tanimoto ($T_c = \\frac{c}{a + b - c}$), Dice, and asymmetric Tversky index.
3. Compute library-scale similarity in milliseconds using C++ accelerated `BulkTanimotoSimilarity`.
4. Build a query-to-library similarity search pipeline that returns ranked 2D structures.
5. Generate similarity maps highlighting the atoms responsible for similarity to a query drug."""),

        ("code", """# Step 0: Imports and Environment Setup
import os
import rdkit
from rdkit import Chem
from rdkit.Chem import Draw, rdFingerprintGenerator
from rdkit import DataStructs
from rdkit.Chem.Draw import SimilarityMaps, IPythonConsole
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

IPythonConsole.ipython_useSVG = True

print(f"RDKit Version: {rdkit.__version__}")"""),

        ("markdown", """## 1. The Chemistry & Math of Molecular Similarity
Given two molecular bit vectors $A$ and $B$:
* $a$ = Number of bits set in molecule $A$
* $b$ = Number of bits set in molecule $B$
* $c$ = Number of shared bits common to both $A$ and $B$ (bitwise AND)

### Similarity Coefficients:
1. **Tanimoto (Jaccard) Index:**
   $$T(A, B) = \\frac{c}{a + b - c}$$
   Range $[0, 1]$. In medicinal chemistry, a Tanimoto similarity $\\ge 0.85$ (using ECFP4) strongly suggests similar biological activity.
2. **Dice Similarity:**
   $$D(A, B) = \\frac{2c}{a + b}$$
3. **Cosine Similarity:**
   $$\\text{Cos}(A, B) = \\frac{c}{\\sqrt{a \\times b}}$$"""),

        ("code", """# Compute pairwise similarities for 3 kinase inhibitors
drugs = {
    "Gefitinib": Chem.MolFromSmiles("COc1cc2ncnc(Nc3ccc(F)c(Cl)c3)c2cc1OCCCN4CCOCC4"),
    "Erlotinib": Chem.MolFromSmiles("C#Cc1cccc(Nc2ncnc3cc(OCCOC)c(OCCOC)cc23)c1"),
    "Aspirin": Chem.MolFromSmiles("CC(=O)Oc1ccccc1C(=O)O")
}

mfpgen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
fps = {name: mfpgen.GetFingerprint(m) for name, m in drugs.items()}

# Pairwise comparisons
sim_gef_erl = DataStructs.TanimotoSimilarity(fps["Gefitinib"], fps["Erlotinib"])
sim_gef_asp = DataStructs.TanimotoSimilarity(fps["Gefitinib"], fps["Aspirin"])

print(f"Tanimoto Similarity (Gefitinib vs Erlotinib): {sim_gef_erl:.4f}  (High - Both EGFR inhibitors)")
print(f"Tanimoto Similarity (Gefitinib vs Aspirin):   {sim_gef_asp:.4f}  (Low - Completely distinct)")"""),

        ("markdown", """## 2. Comparing Similarity Metrics
Let's see how Tanimoto, Dice, and Cosine values compare on the same pair of molecules."""),

        ("code", """fp1, fp2 = fps["Gefitinib"], fps["Erlotinib"]

tanimoto = DataStructs.TanimotoSimilarity(fp1, fp2)
dice = DataStructs.DiceSimilarity(fp1, fp2)
cosine = DataStructs.CosineSimilarity(fp1, fp2)

print(f"Tanimoto: {tanimoto:.4f}")
print(f"Dice:     {dice:.4f}  (Always >= Tanimoto)")
print(f"Cosine:   {cosine:.4f}")"""),

        ("markdown", """## 3. High-Speed Screening: `BulkTanimotoSimilarity`
When searching a library of $100,000+$ molecules, calculating similarity in a Python `for` loop is slow.
`DataStructs.BulkTanimotoSimilarity(query_fp, library_fps)` runs entirely in optimized C++ vector instructions!"""),

        ("code", """# Load real EGFR dataset
candidate_paths = [
    "datasets/EGFR_compounds.csv",
    "../datasets/EGFR_compounds.csv",
    "../../datasets/EGFR_compounds.csv",
    os.path.expanduser("~/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/datasets/EGFR_compounds.csv")
]
csv_path = next((p for p in candidate_paths if os.path.exists(p)), None)

if csv_path:
    df_lib = pd.read_csv(csv_path).head(500) # Sample 500 compounds
    mols = []
    valid_indices = []
    
    for i, s in enumerate(df_lib["smiles"]):
        m = Chem.MolFromSmiles(s)
        if m:
            mols.append(m)
            valid_indices.append(i)
            
    df_clean = df_lib.iloc[valid_indices].reset_index(drop=True)
    lib_fps = [mfpgen.GetFingerprint(m) for m in mols]
    print(f"✅ Generated fingerprints for {len(lib_fps)} library compounds.")"""),

        ("markdown", """## 4. Building a "Find Similar Drugs" Search Engine
Let's build a clean function that takes any query drug SMILES, screens the library in milliseconds, and returns the top-K most similar candidates!"""),

        ("code", """def find_similar_molecules(query_smiles, library_mols, library_fps, library_df, top_k=5):
    query_mol = Chem.MolFromSmiles(query_smiles)
    if not query_mol:
        raise ValueError("Invalid query SMILES!")
        
    query_fp = mfpgen.GetFingerprint(query_mol)
    
    # Fast bulk Tanimoto similarity
    sim_scores = DataStructs.BulkTanimotoSimilarity(query_fp, library_fps)
    
    # Rank by similarity descending
    top_indices = np.argsort(sim_scores)[::-1][:top_k]
    
    results = []
    hit_mols = []
    legends = []
    
    for rank, idx in enumerate(top_indices, 1):
        score = sim_scores[idx]
        cid = library_df.iloc[idx]["molecule_chembl_id"]
        smi = library_df.iloc[idx]["smiles"]
        p_ic50 = library_df.iloc[idx].get("pIC50", "N/A")
        
        results.append({
            "Rank": rank,
            "ChEMBL_ID": cid,
            "Tanimoto_Similarity": round(score, 4),
            "pIC50": p_ic50,
            "SMILES": smi
        })
        hit_mols.append(library_mols[idx])
        legends.append(f"#{rank} {cid}\\nSim: {score:.3f}")
        
    df_results = pd.DataFrame(results)
    return df_results, hit_mols, legends

# Search using Erlotinib as the query drug
erlotinib_smi = "C#Cc1cccc(Nc2ncnc3cc(OCCOC)c(OCCOC)cc23)c1"
df_hits, hit_mols, hit_legends = find_similar_molecules(
    erlotinib_smi, mols, lib_fps, df_clean, top_k=6
)

print("=== 🎯 TOP 6 SIMILAR HITS TO ERLOTINIB ===")
display(df_hits[["Rank", "ChEMBL_ID", "Tanimoto_Similarity", "pIC50"]])

# Visualize top hits
Draw.MolsToGridImage(hit_mols, legends=hit_legends, molsPerRow=3, subImgSize=(300, 200))"""),

        ("markdown", """## 5. Visualizing Similarity Maps (Riniker & Landrum)
Why are two molecules similar? Which atoms contribute most to their high Tanimoto score?
**Similarity Maps** compute atom-level weightings and render a contour heatmap across the 2D chemical structure!"""),

        ("code", """# Create a similarity map for Erlotinib relative to Gefitinib
from rdkit.Chem.Draw import rdMolDraw2D
from IPython.display import SVG

ref_mol = Chem.MolFromSmiles("COc1cc2ncnc(Nc3ccc(F)c(Cl)c3)c2cc1OCCCN4CCOCC4") # Gefitinib
probe_mol = Chem.MolFromSmiles("C#Cc1cccc(Nc2ncnc3cc(OCCOC)c(OCCOC)cc23)c1") # Erlotinib

d2d_sim = rdMolDraw2D.MolDraw2DSVG(450, 350)
SimilarityMaps.GetSimilarityMapForFingerprint(
    ref_mol, probe_mol, SimilarityMaps.GetMorganFingerprint, draw2d=d2d_sim
)
d2d_sim.FinishDrawing()
SVG(d2d_sim.GetDrawingText())"""),

        ("markdown", """## 6. 🎯 Video Hands-On Challenge & Solution
### Problem:
1. Plot the histogram of all 500 Tanimoto similarity scores against Erlotinib.
2. Determine how many molecules in the library have a Tanimoto similarity $\\ge 0.60$.
3. Compute the mean and maximum similarity score across the library."""),

        ("code", """query_fp = mfpgen.GetFingerprint(Chem.MolFromSmiles(erlotinib_smi))
all_sims = np.array(DataStructs.BulkTanimotoSimilarity(query_fp, lib_fps))

num_high_sim = np.sum(all_sims >= 0.60)
print(f"Molecules with Tanimoto >= 0.60: {num_high_sim}")
print(f"Mean similarity:                {np.mean(all_sims):.4f}")
print(f"Maximum similarity:             {np.max(all_sims):.4f}")

plt.figure(figsize=(9, 5))
plt.hist(all_sims, bins=30, color="#2b5c8f", edgecolor="black", alpha=0.8)
plt.axvline(0.60, color="red", linestyle="--", label="Similarity Threshold (0.60)")
plt.xlabel("Tanimoto Similarity to Erlotinib")
plt.ylabel("Compound Count")
plt.title("Chemical Library Similarity Distribution")
plt.legend()
plt.show()"""),

        ("markdown", """## 7. Summary & Key Takeaways
* **Tanimoto Similarity** is the industry standard for chemical fingerprint comparison ($0.85+$ usually indicates analogous biological activity).
* **`BulkTanimotoSimilarity`** enables lightning-fast screening of hundreds of thousands of molecules in fractions of a second.
* **Similarity Maps** provide atom-level explainability for medicinal chemists, revealing which functional groups match the reference template.

**Next Up in Video 09:** **SMARTS & Substructure Searching** — identifying functional groups, searching pharmacophores, and highlighting matched sub-graphs!""")
    ]
    return create_nb(cells)

# ==============================================================================
# VIDEO 09: SMARTS Grammar & Substructure Searching
# ==============================================================================
def build_video_09():
    cells = [
        ("markdown", """# 🎥 Video 09: SMARTS Grammar & Substructure Searching
**RDKit Masterclass — From Zero to Drug Discovery AI**
* **Duration:** ~25 - 30 Minutes
* **Curriculum Level:** LEVEL 4 — SMARTS & Substructure Search (Topics 20, 21, 22, 24)
* **Target Audience:** Cheminformatics Engineers, Medicinal Chemists, Computational Biologists

---

### ⏱️ Video Agenda & Timestamps
* **00:00 - 05:00** | SMILES vs SMARTS: Molecular Representation vs Chemical Pattern Matching
* **05:00 - 10:00** | SMARTS Syntax: Atomic Primitives, Bonds, and Logical Operators
* **10:00 - 14:30** | Substructure Matching: `mol.HasSubstructMatch()` vs `mol.GetSubstructMatches()`
* **14:30 - 19:30** | Detecting 10 Key Medicinal Functional Groups (Alcohols, Amines, Carboxylic acids, etc.)
* **19:30 - 24:30** | Highlighting Matched Substructures in 2D Structure Grids
* **24:30 - 27:30** | Pharmacophore Search in a Large Compound Library
* **27:30 - 30:00** | Hands-On Challenge & Summary

---

### 🎯 Learning Objectives
1. Understand the difference between SMILES (exact molecule) and SMARTS (query pattern with wildcard logic).
2. Master SMARTS grammar: atomic symbols (`c`, `[#6]`), valence (`v`), ring membership (`r`), and logical operators (`!`, `&`, `,`).
3. Query molecules programmatically with `HasSubstructMatch()` and extract atom indices with `GetSubstructMatches()`.
4. Build a comprehensive functional group detector for automated chemical classification.
5. Highlight matched pharmacophore motifs in 2D grid depictions."""),

        ("code", """# Step 0: Imports and Environment Setup
import os
import rdkit
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import IPythonConsole
import pandas as pd

IPythonConsole.ipython_useSVG = True
IPythonConsole.molSize = (320, 220)

print(f"RDKit Version: {rdkit.__version__}")"""),

        ("markdown", """## 1. SMILES vs SMARTS
* **SMILES:** Describes a complete, concrete molecule (e.g. `CCO` is ethanol).
* **SMARTS (SMiles ARbitrary Target Specification):** An extension of SMILES designed to express **queries, structural patterns, and substructures**.
  * `[#6]` = Any Carbon atom (aliphatic or aromatic).
  * `[#7]` = Any Nitrogen atom.
  * `[OH]` = An Oxygen with exactly one hydrogen (Alcohol or Acid).
  * `[!#6]` = Any heteroatom (NOT Carbon).
  * `[r5]` = An atom in a 5-membered ring."""),

        ("code", """# Load Paracetamol and create a SMARTS query for Phenol core
paracetamol = Chem.MolFromSmiles("CC(=O)Nc1ccc(O)cc1")
phenol_smarts = Chem.MolFromSmarts("c1ccc(O)cc1")

has_match = paracetamol.HasSubstructMatch(phenol_smarts)
print(f"Does Paracetamol contain a Phenol core? {has_match}")

matches = paracetamol.GetSubstructMatches(phenol_smarts)
print(f"Matched atom indices: {matches}")"""),

        ("markdown", """## 2. Detecting Key Medicinal Functional Groups
Let's build a functional group detector dictionary using SMARTS patterns."""),

        ("code", """functional_groups = {
    "Alcohol": "[OX2H]",
    "Primary Amine": "[NX3;H2;!$(NC=O)]",
    "Secondary Amine": "[NX3;H1;!$(NC=O)]",
    "Tertiary Amine": "[NX3;H0;!$(NC=O)]",
    "Carboxylic Acid": "[CX3](=O)[OX2H1]",
    "Ester": "[CX3](=O)[OX2H0][#6]",
    "Amide": "[NX3][CX3](=[OX1])[#6]",
    "Aromatic Ring": "a1aaaaa1",
    "Sulfonamide": "[#16X4](=[OX1])(=[OX1])([#7])",
    "Halogen": "[F,Cl,Br,I]"
}

# Compile SMARTS queries
compiled_patterns = {name: Chem.MolFromSmarts(smarts) for name, smarts in functional_groups.items()}

# Profile Ibuprofen, Aspirin, and Paracetamol
drugs = {
    "Aspirin": Chem.MolFromSmiles("CC(=O)Oc1ccccc1C(=O)O"),
    "Ibuprofen": Chem.MolFromSmiles("CC(C)Cc1ccc(cc1)C(C)C(=O)O"),
    "Paracetamol": Chem.MolFromSmiles("CC(=O)Nc1ccc(O)cc1")
}

profiling_results = []
for drug_name, mol in drugs.items():
    row = {"Drug": drug_name}
    for fg_name, pattern in compiled_patterns.items():
        row[fg_name] = len(mol.GetSubstructMatches(pattern))
    profiling_results.append(row)

df_fg = pd.DataFrame(profiling_results)
print("=== 📋 FUNCTIONAL GROUP DETECTION MATRIX ===")
display(df_fg)"""),

        ("markdown", """## 3. Highlighting Substructure Matches in 2D Grids
When presenting hits to medicinal chemists, visually highlighting the matched core substructure is essential."""),

        ("code", """# Highlight the Carboxylic Acid group in Aspirin and Ibuprofen
acid_smarts = Chem.MolFromSmarts("[CX3](=O)[OX2H1]")

mols_to_draw = [drugs["Aspirin"], drugs["Ibuprofen"]]
matched_atom_lists = [m.GetSubstructMatch(acid_smarts) for m in mols_to_draw]
legends = ["Aspirin (Carboxylic Acid Highlighted)", "Ibuprofen (Carboxylic Acid Highlighted)"]

Draw.MolsToGridImage(
    mols_to_draw,
    legends=legends,
    highlightAtomLists=matched_atom_lists,
    molsPerRow=2,
    subImgSize=(350, 220)
)"""),

        ("markdown", """## 4. Screening a Chemical Library for a Pharmacophore Core
Let's search our EGFR dataset for compounds containing the **4-anilinoquinazoline kinase hinge-binder core**."""),

        ("code", """# 4-anilinoquinazoline core SMARTS
# Pyrimidine ring with two nitrogens, fused to benzene, substituted with an aromatic amine (NH-c)
quinazoline_core_smarts = Chem.MolFromSmarts("c1ccc2ncnc(Nc3ccccc3)c2c1")

candidate_paths = [
    "datasets/EGFR_compounds.csv",
    "../datasets/EGFR_compounds.csv",
    "../../datasets/EGFR_compounds.csv",
    os.path.expanduser("~/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/datasets/EGFR_compounds.csv")
]
csv_path = next((p for p in candidate_paths if os.path.exists(p)), None)

if csv_path:
    df_egfr = pd.read_csv(csv_path).head(300)
    matching_compounds = []
    
    for _, row in df_egfr.iterrows():
        m = Chem.MolFromSmiles(row["smiles"])
        if m and m.HasSubstructMatch(quinazoline_core_smarts):
            matching_compounds.append((row["molecule_chembl_id"], m, row.get("pIC50", "N/A")))
            
    print(f"Found {len(matching_compounds)} compounds containing the 4-anilinoquinazoline core!")
    
    # Draw first 4 matching hits with highlights
    if matching_compounds:
        sample_hits = matching_compounds[:4]
        hit_mols = [item[1] for item in sample_hits]
        hit_highlights = [m.GetSubstructMatch(quinazoline_core_smarts) for m in hit_mols]
        hit_legends = [f"{item[0]}\\npIC50: {item[2]}" for item in sample_hits]
        
        display(Draw.MolsToGridImage(
            hit_mols,
            legends=hit_legends,
            highlightAtomLists=hit_highlights,
            molsPerRow=4,
            subImgSize=(280, 200)
        ))"""),

        ("markdown", """## 5. 🎯 Video Hands-On Challenge & Solution
### Problem:
Define a SMARTS pattern for **Sulfonamides** (`S(=O)(=O)N`), search a list of 4 drugs, and determine which ones contain a sulfonamide group, highlighting the matched atoms."""),

        ("code", """challenge_mols = {
    "Sildenafil (Viagra)": "CCCC1=NN(C)C2=C1N=C(NC2=O)C3=C(OCC)C=CC(=C3)S(=O)(=O)N4CCN(C)CC4",
    "Celecoxib (Celebrex)": "CC1=CC=C(C=C1)C2=CC(=NN2C3=CC=C(C=C3)S(=O)(=O)N)C(F)(F)F",
    "Aspirin": "CC(=O)Oc1ccccc1C(=O)O",
    "Gefitinib": "COc1cc2ncnc(Nc3ccc(F)c(Cl)c3)c2cc1OCCCN4CCOCC4"
}

sulfonamide_smarts = Chem.MolFromSmarts("S(=O)(=O)[NX3]")

mols_list = []
matched_atoms_list = []
legends_list = []

for name, smi in challenge_mols.items():
    m = Chem.MolFromSmiles(smi)
    match = m.GetSubstructMatch(sulfonamide_smarts)
    has_grp = len(match) > 0
    
    mols_list.append(m)
    matched_atoms_list.append(match if has_grp else [])
    status = "YES (Sulfonamide)" if has_grp else "NO"
    legends_list.append(f"{name}\\n{status}")

Draw.MolsToGridImage(
    mols_list,
    legends=legends_list,
    highlightAtomLists=matched_atoms_list,
    molsPerRow=2,
    subImgSize=(350, 240)
)"""),

        ("markdown", """## 6. Summary & Key Takeaways
* **SMARTS** is the regex of chemistry: it lets you search for substructural patterns, generic atom types, and ring topologies.
* `mol.HasSubstructMatch(query)` returns a fast boolean check; `mol.GetSubstructMatches(query)` returns the matched atom indices.
* Combining SMARTS queries allows building automated functional group classifiers and medicinal chemistry filter catalogs.

**Next Up in Video 10:** **Molecular Standardization & Dataset Curation Pipeline** — salt stripping, charge neutralization, tautomer canonicalization, and deduplication!""")
    ]
    return create_nb(cells)

# ==============================================================================
# VIDEO 10: Molecule Standardization & Curation Pipeline
# ==============================================================================
def build_video_10():
    cells = [
        ("markdown", """# 🎥 Video 10: Molecular Standardization & Curation Pipeline
**RDKit Masterclass — From Zero to Drug Discovery AI**
* **Duration:** ~25 - 30 Minutes
* **Curriculum Level:** LEVEL 5 — Chemical Data Processing (Topics 26, 27, 28, 29)
* **Target Audience:** Cheminformatics Engineers, AI Researchers, Data Curators

---

### ⏱️ Video Agenda & Timestamps
* **00:00 - 04:30** | Why Chemical Data Curation is Crucial for AI ("Garbage In, Garbage Out")
* **04:30 - 09:30** | The Anatomy of Dirty Data: Mixtures, Counterions, Non-Standard Charges
* **09:30 - 14:00** | Salt Stripping & Solvent Removal using `SaltRemover` & Largest Fragment Chooser
* **14:00 - 18:30** | Normalizing Functional Groups with `rdMolStandardize.Normalizer`
* **18:30 - 23:00** | Charge Neutralization & Zwitterion Handling
* **23:00 - 27:00** | Tautomer Canonicalization with `TautomerEnumerator`
* **27:00 - 30:00** | Building an End-to-End Production Curation Pipeline

---

### 🎯 Learning Objectives
1. Understand why public datasets (ChEMBL, PubChem, ZINC) require rigorous standardization before Machine Learning.
2. Remove salts, counterions, and solvent adducts systematically.
3. Normalize non-standard representations (nitro groups, sulfoxides, azides) with `rdMolStandardize.Normalizer`.
4. Neutralize charged species (carboxylates, amine salts) to their parent neutral forms.
5. Canonicalize tautomers to prevent artificial data leakage and false duplicate entries."""),

        ("code", """# Step 0: Imports and Environment Setup
import rdkit
from rdkit import Chem
from rdkit.Chem import Draw, SaltRemover
from rdkit.Chem.MolStandardize import rdMolStandardize
from rdkit.Chem.Draw import IPythonConsole
import pandas as pd

IPythonConsole.ipython_useSVG = True
IPythonConsole.molSize = (320, 220)

print(f"RDKit Version: {rdkit.__version__}")"""),

        ("markdown", """## 1. The Standardization Workflow
A robust cheminformatics standardization pipeline follows 5 rigorous steps:
1. **Sanitization Check:** Ensure valences and aromaticity are valid.
2. **Salt & Solvent Stripping:** Remove counterions (e.g. $Na^+, Cl^-, TFA$) and isolate the largest organic fragment.
3. **Normalization:** Convert functional groups to standard valence bond representations.
4. **Charge Neutralization:** Convert uncharged counterion remnants into neutral species without breaking true zwitterions.
5. **Tautomer Canonicalization:** Resolve tautomeric equilibria (e.g., keto-enol, lactam-lactim) to a single canonical tautomer."""),

        ("code", """# Example of messy input: Sildenafil citrate salt with non-standard nitro/oxide groups
messy_smi = "CCCC1=NN(C)C2=C1N=C(NC2=O)C3=C(OCC)C=CC(=C3)S(=O)(=O)N4CCN(C)CC4.C(C(=O)O)C(CC(=O)O)(C(=O)O)O"
messy_mol = Chem.MolFromSmiles(messy_smi)

print("Original heavy atoms (including Citrate salt):", messy_mol.GetNumAtoms())"""),

        ("markdown", """## 2. Step 1: Fragment Parent Extraction (Salt & Solvent Stripping)
`rdMolStandardize.FragmentParent(mol)` automatically strips inorganic counterions and returns the largest organic covalent component."""),

        ("code", """# Extract parent molecule
parent_mol = rdMolStandardize.FragmentParent(messy_mol)
print("After FragmentParent (API only):", parent_mol.GetNumAtoms())
print("Canonical SMILES:", Chem.MolToSmiles(parent_mol))

Draw.MolsToGridImage([messy_mol, parent_mol], legends=["Before: With Citrate Salt", "After: Parent API"])"""),

        ("markdown", """## 3. Step 2: Normalization
Different chemists represent nitro groups, sulfoxides, and azides differently (e.g. hypervalent vs charge-separated).
`rdMolStandardize.Normalizer()` standardizes all functional groups to standard IUPAC conventions."""),

        ("code", """normalizer = rdMolStandardize.Normalizer()

# Molecule with non-standard charge representations
non_standard_nitro = Chem.MolFromSmiles("c1ccccc1[N+](=O)[O-]") # Standard
normalized_mol = normalizer.normalize(parent_mol)

print("Normalized successfully!")"""),

        ("markdown", """## 4. Step 3: Charge Neutralization
Often salts or bases leave molecules in charged states (e.g., $COO^-$ or $NH_3^+$).
`rdMolStandardize.Uncharger()` neutralizes charged species while preserving zwitterions (like amino acids)."""),

        ("code", """uncharger = rdMolStandardize.Uncharger()

# Test on charged carboxylate and quaternary amine salt
charged_smiles = [
    ("Sodium Benzoate [O-]", "c1ccccc1C(=O)[O-]"),
    ("Protonated Amine [NH3+]", "CC[NH3+]"),
    ("Zwitterionic Alanine", "C[C@@H]([NH3+])C(=O)[O-]")
]

neutralized_results = []
for name, smi in charged_smiles:
    m = Chem.MolFromSmiles(smi)
    m_neut = uncharger.uncharge(m)
    neutralized_results.append({
        "Name": name,
        "Original_SMILES": Chem.MolToSmiles(m),
        "Neutralized_SMILES": Chem.MolToSmiles(m_neut)
    })

df_neut = pd.DataFrame(neutralized_results)
display(df_neut)"""),

        ("markdown", """## 5. Step 4: Tautomer Canonicalization
A single chemical compound can exist in multiple tautomeric forms in solution (e.g. 2-pyridone vs 2-hydroxypyridine).
Without tautomer canonicalization, the same molecule could be treated as two distinct entities, causing severe **data leakage** in train/test splits!"""),

        ("code", """te = rdMolStandardize.TautomerEnumerator()

# 2-Pyridone vs 2-Hydroxypyridine
pyridone = Chem.MolFromSmiles("O=C1C=CC=CN1")
hydroxypyridine = Chem.MolFromSmiles("Oc1ccccn1")

canon_1 = te.Canonicalize(pyridone)
canon_2 = te.Canonicalize(hydroxypyridine)

print("Pyridone canonical SMILES:        ", Chem.MolToSmiles(canon_1))
print("Hydroxypyridine canonical SMILES: ", Chem.MolToSmiles(canon_2))
print("Are both canonical tautomers identical?", Chem.MolToSmiles(canon_1) == Chem.MolToSmiles(canon_2))

Draw.MolsToGridImage([pyridone, hydroxypyridine, canon_1], legends=["2-Pyridone", "2-Hydroxypyridine", "Canonical Form"])"""),

        ("markdown", """## 6. The Complete Production Curation Class
Let's assemble a unified `MoleculeCurator` class ready for deployment in production pipelines."""),

        ("code", """class MoleculeCurator:
    def __init__(self):
        self.normalizer = rdMolStandardize.Normalizer()
        self.uncharger = rdMolStandardize.Uncharger()
        self.tautomer_enumerator = rdMolStandardize.TautomerEnumerator()
        
    def curate(self, smiles):
        if not isinstance(smiles, str) or not smiles.strip():
            return None, "Empty or invalid string"
            
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None, "Sanitization/parsing failure"
            
        try:
            # 1. Strip salts and isolate largest organic fragment
            parent = rdMolStandardize.FragmentParent(mol)
            
            # 2. Normalize functional groups
            normalized = self.normalizer.normalize(parent)
            
            # 3. Neutralize charges
            uncharged = self.uncharger.uncharge(normalized)
            
            # 4. Canonicalize tautomer
            canonical_tautomer = self.tautomer_enumerator.Canonicalize(uncharged)
            
            # 5. Final canonical SMILES
            final_smi = Chem.MolToSmiles(canonical_tautomer)
            return final_smi, "Success"
        except Exception as e:
            return None, f"Pipeline Error: {str(e)}"

# Test the curator on a messy multi-component set
curator = MoleculeCurator()
messy_dataset = [
    "c1ccccc1C(=O)[O-].[Na+]",           # Sodium benzoate
    "O=C1C=CC=CN1",                      # 2-Pyridone
    "Oc1ccccn1",                         # 2-Hydroxypyridine (duplicate tautomer)
    "CN(C)C(=N)NC(=N)N.Cl",              # Metformin HCl
    "C1(=O)(=O)(=O)C"                   # Chemically invalid
]

curated_results = []
for s in messy_dataset:
    clean_smi, status = curator.curate(s)
    curated_results.append({
        "Input_SMILES": s,
        "Status": status,
        "Curated_SMILES": clean_smi
    })

df_curated = pd.DataFrame(curated_results)
print("=== 🧪 MOLECULE CURATION RESULTS ===")
display(df_curated)"""),

        ("markdown", """## 7. 🎯 Video Hands-On Challenge & Solution
### Problem:
Take a collection of 3 compounds with varying salt counterions and tautomers:
1. Run them through the `MoleculeCurator`.
2. Deduplicate using the resulting canonical SMILES.
3. Output the final unique compound count and 2D grid image."""),

        ("code", """test_compounds = [
    "CC(=O)Oc1ccccc1C(=O)O.Na",        # Aspirin Sodium
    "CC(=O)Oc1ccccc1C(=O)O",           # Aspirin Neutral (duplicate)
    "CC(C)Cc1ccc(cc1)C(C)C(=O)O.Cl",   # Ibuprofen HCl
    "CC(C)Cc1ccc(cc1)C(C)C(=O)O",      # Ibuprofen Neutral (duplicate)
    "Oc1ccccn1"                        # 2-Hydroxypyridine
]

unique_curated = {}
for smi in test_compounds:
    clean_smi, status = curator.curate(smi)
    if status == "Success":
        if clean_smi not in unique_curated:
            unique_curated[clean_smi] = Chem.MolFromSmiles(clean_smi)

print(f"Original count: {len(test_compounds)} records")
print(f"Unique curated compounds: {len(unique_curated)}")

Draw.MolsToGridImage(
    list(unique_curated.values()),
    legends=[f"Curated #{i+1}\\n{s}" for i, s in enumerate(unique_curated.keys())],
    molsPerRow=3,
    subImgSize=(300, 200)
)"""),

        ("markdown", """## 8. Summary & Key Takeaways
* **Raw chemical datasets are messy:** Salt adducts, non-standard functional group charges, and tautomer duplicates confound machine learning models.
* **`rdMolStandardize.FragmentParent`** strips salts and solvents reliably.
* **`TautomerEnumerator.Canonicalize`** maps diverse tautomers to a unique canonical form.
* Deploying a standard `MoleculeCurator` ensures pristine data quality for training QSAR and deep learning models.

**Next Up in Video 11:** **Chemical Space Exploration, Dimensionality Reduction & Clustering** — PCA, t-SNE, UMAP, and Taylor-Butina clustering!""")
    ]
    return create_nb(cells)

# ==============================================================================
# MAIN RUNNER FOR VIDEOS 06 TO 10
# ==============================================================================
if __name__ == "__main__":
    base_dir = "/home/softvence/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/RDKit Tutorials"
    
    video_configs = [
        ("05_Lipinski_Drug_Likeness_Analysis/Video_06_Drug_Likeness_Rules_and_MedChem_Filters.ipynb", build_video_06),
        ("06_Molecular_Fingerprints/Video_07_Molecular_Fingerprints_Deep_Dive.ipynb", build_video_07),
        ("07_Similarity_Search/Video_08_Molecular_Similarity_and_Similarity_Searching.ipynb", build_video_08),
        ("08_Substructure_Search/Video_09_SMARTS_and_Substructure_Searching.ipynb", build_video_09),
        ("09_Molecule_Standardization/Video_10_Molecule_Standardization_and_Curation_Pipeline.ipynb", build_video_10)
    ]
    
    for rel_path, builder_func in video_configs:
        full_path = os.path.join(base_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        nb = builder_func()
        with open(full_path, "w", encoding="utf-8") as f:
            nbf.write(nb, f)
        print(f"Generated: {rel_path} ({len(nb.cells)} cells)")
