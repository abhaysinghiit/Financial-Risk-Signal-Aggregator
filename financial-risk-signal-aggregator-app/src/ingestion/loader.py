from pathlib import Path
import json
import pandas as pd

def load_file(file_path):

    path = Path(file_path)

    suffix = path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(path)

    elif suffix == ".json":

        with open(path, "r") as f:
            return json.load(f)

    elif suffix == ".txt":

        with open(path, "r") as f:
            return f.read()

    raise ValueError(
        f"Unsupported file type {suffix}"
    )