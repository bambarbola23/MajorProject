import os

BASE_DIR = r"d:\Projects 2026 All\Major Project\phase1_prep"

# List of all directories to create
dirs = [
    BASE_DIR,
    os.path.join(BASE_DIR, "architecture"),
    os.path.join(BASE_DIR, "modules"),
    os.path.join(BASE_DIR, "implementation"),
    os.path.join(BASE_DIR, "ml"),
    os.path.join(BASE_DIR, "review"),
    os.path.join(BASE_DIR, "diagrams")
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

print("Created directories successfully.")
