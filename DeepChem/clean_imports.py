import nbformat

nb_path = "DeepChem.ipynb"
with open(nb_path, "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

changed = False
for cell in nb.cells:
    if cell.cell_type == "code":
        new_source = []
        for line in cell.source.split('\n'):
            if line.strip().startswith("from deepchem") or line.strip().startswith("import deepchem"):
                try:
                    exec(line)
                    new_source.append(line)
                except Exception as e:
                    print(f"Removing invalid import: {line.strip()} - Error: {e}")
                    changed = True
            else:
                new_source.append(line)
        cell.source = '\n'.join(new_source)
        cell.outputs = []
        cell.execution_count = None

if changed:
    with open(nb_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print("Notebook updated by removing failing imports.")
else:
    print("No failing imports found.")
