from pathlib import Path
import json
import sys
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spotify_features import load_dataset, clean_dataset, get_reference_stats

DATA_PATH = ROOT / "spotify_playlists.csv"
ARTIFACTS = ROOT / "deployment" / "artifacts"
MODEL_PATH = ARTIFACTS / "spotify_playlist_model.joblib"
METADATA_PATH = ARTIFACTS / "model_metadata.json"
STATS_PATH = ARTIFACTS / "reference_stats.json"

def main():
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    df = clean_dataset(load_dataset(DATA_PATH))
    cols = {str(c).lower(): c for c in df.columns}
    # Dataset Kaggle ini umumnya memakai artistname, trackname, playlistname.
    track_col = cols.get("trackname") or cols.get("track_name")
    artist_col = cols.get("artistname") or cols.get("artist_name")
    playlist_col = cols.get("playlistname") or cols.get("playlist_name")
    if not track_col:
        raise ValueError(f"Kolom judul lagu tidak ditemukan. Kolom tersedia: {list(df.columns)}")
    text_cols = [c for c in [track_col, artist_col, playlist_col] if c]
    text = df[text_cols].fillna("").astype(str).agg(" ".join, axis=1).str.strip()
    valid = text.str.len() > 0
    text = text[valid].reset_index(drop=True)
    if len(text) < 2:
        raise ValueError("Dataset harus memiliki minimal dua baris berisi teks untuk melatih model.")
    model = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=100000, stop_words=None)),
        ("neighbors", NearestNeighbors(metric="cosine", algorithm="brute", n_neighbors=min(6, len(text))))
    ])
    model.fit(text)
    joblib.dump({"pipeline": model, "documents": text.tolist()}, MODEL_PATH)
    metadata = {
        "project": "Spotify Playlists",
        "model_type": "TF-IDF + Nearest Neighbors",
        "purpose": "Menemukan baris lagu/playlist yang teksnya mirip; bukan prediksi jumlah streaming.",
        "source_dataset": "Kaggle andrewmvd/spotify-playlists",
        "rows_used": int(len(text)),
        "text_columns": [str(c) for c in text_cols],
        "trained": True
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    STATS_PATH.write_text(json.dumps(get_reference_stats(df), indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Model disimpan: {MODEL_PATH}")
    print(f"Metadata disimpan: {METADATA_PATH}")
    print(f"Statistik disimpan: {STATS_PATH}")

if __name__ == "__main__":
    main()
