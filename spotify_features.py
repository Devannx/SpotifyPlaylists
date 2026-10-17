from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = ROOT / "spotify_playlists.csv"

def load_dataset(path=DEFAULT_DATA_PATH):
    """Muat dataset Spotify Playlists dari file CSV."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset tidak ditemukan: {path}. Simpan CSV sebagai spotify_playlists.csv di folder utama."
        )
    return pd.read_csv(path, low_memory=False)

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan nama kolom, spasi teks, baris duplikat, dan baris kosong penuh."""
    cleaned = df.copy()
    cleaned.columns = [str(col).strip().lower().replace(" ", "_") for col in cleaned.columns]

    for col in cleaned.select_dtypes(include=["object", "string"]).columns:
        cleaned[col] = cleaned[col].map(lambda value: value.strip() if isinstance(value, str) else value)
        cleaned[col] = cleaned[col].replace("", pd.NA)

    cleaned = cleaned.dropna(how="all").drop_duplicates().reset_index(drop=True)
    return cleaned

def dataset_summary(df: pd.DataFrame) -> dict:
    """Kembalikan ringkasan dasar dataset."""
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "missing_cells": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }

if __name__ == "__main__":
    data = load_dataset()
    cleaned = clean_dataset(data)
    print("Ringkasan data asli:", dataset_summary(data))
    print("Ringkasan setelah cleaning:", dataset_summary(cleaned))
    output = ROOT / "spotify_playlists_cleaned.csv"
    cleaned.to_csv(output, index=False)
    print(f"Data bersih disimpan ke: {output}")
