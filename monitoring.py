from datetime import datetime, timezone
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "spotify_playlists.csv"
OUTPUT_PATH = ROOT / "deployment" / "artifacts" / "data_quality_report.json"

def main():
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_file": DATA_PATH.name,
        "dataset_exists": DATA_PATH.exists(),
    }

    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH, low_memory=False)
        report.update({
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "missing_cells": int(df.isna().sum().sum()),
            "duplicate_rows": int(df.duplicated().sum()),
            "columns_detail": {
                str(col): {
                    "dtype": str(df[col].dtype),
                    "missing": int(df[col].isna().sum()),
                    "unique": int(df[col].nunique(dropna=True)),
                }
                for col in df.columns
            },
        })

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
