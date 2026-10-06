# 🎬 RDKit Masterclass Video Playlist: Zero to Drug Discovery AI
### A Comprehensive 15-Episode Video Course (~25-30 Mins Each) + 2 End-to-End Capstone Projects

Welcome to the definitive hands-on training series for **RDKit, Cheminformatics, and AI for Drug Discovery**. This playlist is designed for students, bioinformaticians, data scientists, and computational chemists transitioning into AI-driven molecular modeling.

Each video lesson is calibrated for a **25 to 30-minute instructional session**, complete with chemical theory, live code walkthroughs, visual outputs, debugging tips, and practical hands-on exercises with solutions.

---

## 📑 Master Playlist Catalog

| Ep | Video Title | Est. Time | Curriculum Level | Notebook Link | Key Topics & RDKit APIs |
|:---:|:---|:---:|:---:|:---|:---|
| **01** | **RDKit Fundamentals & Molecular Representations** | 28 min | Level 1 (01-04) | [Video_01.ipynb](file:///home/softvence/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/RDKit%20Tutorials/01_Molecule_Representation/Video_01_RDKit_Fundamentals_and_Molecular_Objects.ipynb) | Mol objects, Atoms & Bonds, SMILES, SMARTS, InChI/InChIKey, `MolFromSmiles`, canonicalization, kekulization |
| **02** | **Molecular File Formats & I/O Operations** | 26 min | Level 1 (06) & Level 5 (25) | [Video_02.ipynb](file:///home/softvence/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/RDKit%20Tutorials/02_SMILES_MOL_SDF_Handling/Video_02_Molecular_File_Formats_and_IO.ipynb) | SDF, MOL (V2000), SMI, CSV, `SDMolSupplier`, `ForwardSDMolSupplier`, SD tags, `SDWriter`, `PandasTools` |
| **03** | **Molecular Sanitization, Cleaning & QC** | 27 min | Level 1 (07) & Level 5 (26-29) | [Video_03.ipynb](file:///home/softvence/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/RDKit%20Tutorials/03_Data_Loading_and_Cleaning/Video_03_Molecular_Sanitization_and_Cleaning.ipynb) | The 8 sanitization steps, debugging valence errors, `sanitize=False`, `SaltRemover`, API isolation, Dataset QC pipeline |
| **04** | **2D Molecular Visualization & Rendering** | 25 min | Level 1 (05) & Level 8 (47) | [Video_04.ipynb](file:///home/softvence/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/RDKit%20Tutorials/13_Molecular_Visualization/Video_04_2D_Molecular_Visualization_and_Rendering.ipynb) | `Compute2DCoords`, `MolsToGridImage`, custom atom/bond RGB highlights, `rdMolDraw2D` SVG export, reaction drawing |
| **05** | **Physicochemical Descriptors & Property Distributions** | 28 min | Level 2 (08, 10-12) | [Video_05.ipynb](file:///home/softvence/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/RDKit%20Tutorials/04_Molecular_Descriptors_and_Properties/Video_05_Physicochemical_Properties_and_Descriptors.ipynb) | MW, MolLogP, TPSA, HBD, HBA, RotBonds, Fraction Csp3, BertzCT, batch `Descriptors._descList` pipeline, property histograms |
| **06** | **Drug-Likeness Rules & MedChem Filters** | 29 min | Level 2 (09) & Level 4 (23) | [Video_06.ipynb](file:///home/softvence/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/RDKit%20Tutorials/05_Lipinski_Drug_Likeness_Analysis/Video_06_Drug_Likeness_Rules_and_MedChem_Filters.ipynb) | Lipinski Rule of 5, Veber bioavailability, PAINS & Brenk alerts via `FilterCatalog`, multi-parametric radar charts |
| **07** | **Molecular Fingerprints Deep Dive** | 30 min | Level 3 (13-17) | [Video_07.ipynb](file:///home/softvence/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/RDKit%20Tutorials/06_Molecular_Fingerprints/Video_07_Molecular_Fingerprints_Deep_Dive.ipynb) | Descriptors vs Fingerprints, Morgan / ECFP4 vs ECFP6, `rdFingerprintGenerator`, MACCS (166 keys), Topological FP, NumPy vectors |
| **08** | **Chemical Similarity & Similarity Search Engine** | 27 min | Level 3 (18, 19) | [Video_08.ipynb](file:///home/softvence/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/RDKit%20Tutorials/07_Similarity_Search/Video_08_Molecular_Similarity_and_Similarity_Searching.ipynb) | Tanimoto, Dice, Cosine, `BulkTanimotoSimilarity` for fast screening, "Find Similar Drugs" query engine, Riniker similarity maps |
| **09** | **SMARTS Grammar & Substructure Searching** | 28 min | Level 4 (20-22, 24) | [Video_09.ipynb](file:///home/softvence/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/RDKit%20Tutorials/08_Substructure_Search/Video_09_SMARTS_and_Substructure_Searching.ipynb) | SMILES vs SMARTS, atomic primitives, `HasSubstructMatch`, 10 functional group detectors, highlighting matched pharmacophores |
| **10** | **Molecular Standardization & Dataset Curation** | 26 min | Level 5 (26-29) | [Video_10.ipynb](file:///home/softvence/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/RDKit%20Tutorials/09_Molecule_Standardization/Video_10_Molecule_Standardization_and_Curation_Pipeline.ipynb) | `FragmentParent`, `Normalizer`, `Uncharger`, `TautomerEnumerator`, resolving tautomer duplicates, automated curation class |
| **11** | **Chemical Space Exploration & Clustering** | 29 min | Level 6 (30-35) | [Video_11.ipynb](file:///home/softvence/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/RDKit%20Tutorials/10_Scaffold_Analysis/Video_11_Chemical_Space_Visualization_and_Clustering.ipynb) | High-dimensional mapping, PCA vs t-SNE, Taylor-Butina clustering (`Butina.ClusterData`), centroid extraction, `MaxMinPicker` |
| **12** | **Bemis-Murcko Scaffolds & Molecular Decomposition** | 27 min | Level 8 (44-46) | [Video_12.ipynb](file:///home/softvence/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/RDKit%20Tutorials/10_Scaffold_Analysis/Video_12_Scaffold_Analysis_and_Molecular_Decomposition.ipynb) | Murcko scaffolds (`GetScaffoldForMol`), generic frameworks (`MakeScaffoldGeneric`), privileged scaffold ranking, Matched Molecular Pairs |
| **13** | **Chemical Reactions & BRICS Molecular Design** | 28 min | Level 8 (41-43) | [Video_13.ipynb](file:///home/softvence/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/RDKit%20Tutorials/12_Chemical_Reaction_Processing/Video_13_Chemical_Reactions_and_BRICS_Fragmentation.ipynb) | Reaction SMARTS (`ReactionFromSmarts`, `RunReactants`), virtual amide & ester libraries, BRICS 16 cleavage rules, `BRICSBuild` |
| **14** | **3D Conformer Generation & Geometry Optimization** | 28 min | Level 8 (Conformers) | [Video_14.ipynb](file:///home/softvence/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/RDKit%20Tutorials/11_3D_Conformer_Generation/Video_14_3D_Conformers_and_Geometry_Optimization.ipynb) | Explicit Hydrogens (`AddHs`), ETKDG v3 embedding, MMFF94s minimization, ensemble sampling (`EmbedMultipleConfs`), RMSD alignment |
| **15** | **Machine Learning QSAR & Modern AI Representations** | 30 min | Level 7 & Level 10 | [Video_15.ipynb](file:///home/softvence/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/RDKit%20Tutorials/14_QSAR_Machine_Learning/Video_15_Machine_Learning_QSAR_and_Modern_AI.ipynb) | QSAR principles, Bemis-Murcko scaffold splitting, Random Forest $pIC_{50}$ regressor, converting Mol to PyTorch Geometric graph data |

---

## 🏆 Production Capstone Projects

### 🌟 Project 01: End-to-End Virtual Screening & Drug-Likeness Discovery Pipeline
* **Location:** [`Project_01_End_to_End_Virtual_Screening_Pipeline.ipynb`](file:///home/softvence/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/RDKit%20Tutorials/16_End_to_End_Drug_Discovery_Project/Project_01_End_to_End_Virtual_Screening_Pipeline.ipynb)
* **Real-World Goal:** Screen a multi-thousand compound library against the Human Epidermal Growth Factor Receptor (EGFR) kinase target to isolate clinical-grade lead candidates.
* **Pipeline Architecture:**
  1. **Raw Library Ingestion:** Loads candidate chemical records.
  2. **Automated Salt Stripping:** Disconnects counterions and standardizes API structures.
  3. **Physicochemical Filtering:** Lipinski Rule of 5 and Veber Oral Bioavailability rules.
  4. **Medicinal Chemistry Safety:** Eliminates PAINS false-positive assay interferers and reactive Brenk alerts.
  5. **Pharmacophore Matching:** Substructure screening for the 4-anilinoquinazoline hinge-binding motif.
  6. **Molecular Similarity:** Screens Morgan ECFP4 fingerprints against FDA drug Gefitinib ($T_c \ge 0.40$).
  7. **Multi-Parametric Optimization (MPO):** Composite scoring weighting similarity, rigidity, and optimal lipophilicity.
  8. **Deliverables:** Funnel attrition waterfall chart, annotated 2D structure grids, and export to `top_virtual_screening_hits.sdf` and `.csv`.

---

### 🌟 Project 02: Production Machine Learning QSAR & Chemical Space Explorer
* **Location:** [`Project_02_Machine_Learning_QSAR_and_Chemical_Space_Explorer.ipynb`](file:///home/softvence/Projects/AI-Engineer-for-Life-Sciences-Libraries/Cheminformatics/RDKit/RDKit%20Tutorials/16_End_to_End_Drug_Discovery_Project/Project_02_Machine_Learning_QSAR_and_Chemical_Space_Explorer.ipynb)
* **Real-World Goal:** Build an industrial predictive QSAR regression model and 2D chemical space explorer on 4,772 real ChEMBL EGFR compounds with experimental bioactivities.
* **Pipeline Architecture:**
  1. **ChEMBL Ingestion & QC:** Deduplicates multiple assay reports using canonical InChIKeys and consensus median $pIC_{50}$.
  2. **Hybrid Featurization:** Combines 1024-bit Morgan fingerprints (ECFP4) with 10 scaled 2D physicochemical descriptors.
  3. **Scaffold-Based Split:** Implements Bemis-Murcko scaffold splitting to ensure zero data leakage and genuine out-of-scaffold generalization.
  4. **Model Benchmarking:** Trains and benchmarks Random Forest, Gradient Boosting, and Ridge Regressors.
  5. **Rigorous Validation:** Calculates $R^2$, RMSE, MAE, actual vs predicted scatter plots, and residual error distributions.
  6. **High-Dimensional Chemical Space:** Projects the compound collection using 2D t-SNE with continuous potency and categorical activity overlays.
  7. **Prospective Virtual Screening:** Evaluates novel external molecules and prioritizes lead optimization analogs.

---

## 🛠️ Environment Installation & Quickstart

```bash
# 1. Clone or navigate to the repository
cd "/home/softvence/Projects/AI-Engineer-for-Life-Sciences-Libraries"

# 2. Set up environment using uv (fastest) or conda
uv venv .venv --python 3.12
source .venv/bin/activate
uv pip install rdkit pandas numpy scikit-learn matplotlib seaborn jupyter jupyterlab

# 3. Launch JupyterLab to start recording or learning
jupyter lab
```
