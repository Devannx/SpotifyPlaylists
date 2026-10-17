from pathlib import Path
import sys

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "spotify_playlists.csv"

st.set_page_config(page_title="Spotify Playlists Explorer", page_icon="🎵", layout="wide")
st.title("🎵 Spotify Playlists Explorer")
st.write("Dashboard eksplorasi dataset Spotify Playlists dari Kaggle.")

@st.cache_data
def load_data(path: str):
    return pd.read_csv(path, low_memory=False)

if not DATA_PATH.exists():
    st.error(f"File dataset tidak ditemukan: {DATA_PATH.name}")
    st.info("Letakkan file CSV dataset di folder utama proyek dan beri nama spotify_playlists.csv.")
    st.stop()

try:
    df = load_data(str(DATA_PATH))
except Exception as exc:
    st.error(f"Dataset gagal dibaca: {exc}")
    st.stop()

st.subheader("Pratinjau data")
st.caption(f"Ukuran dataset: {df.shape[0]:,} baris × {df.shape[1]} kolom")
st.dataframe(df.head(100), use_container_width=True)

left, middle, right = st.columns(3)
left.metric("Jumlah baris", f"{len(df):,}")
middle.metric("Jumlah kolom", f"{len(df.columns):,}")
right.metric("Sel kosong", f"{int(df.isna().sum().sum()):,}")

st.subheader("Ringkasan kualitas data")
quality = pd.DataFrame({
    "Kolom": df.columns,
    "Tipe data": [str(t) for t in df.dtypes],
    "Nilai kosong": [int(df[c].isna().sum()) for c in df.columns],
    "Nilai unik": [int(df[c].nunique(dropna=True)) for c in df.columns],
})
st.dataframe(quality, use_container_width=True)

st.subheader("Analisis kolom kategori")
text_columns = df.select_dtypes(include=["object", "string"]).columns.tolist()
if text_columns:
    selected_column = st.selectbox("Pilih kolom untuk melihat nilai yang paling sering muncul", text_columns)
    top_n = st.slider("Jumlah kategori", min_value=5, max_value=30, value=10)
    counts = df[selected_column].fillna("(Kosong)").astype(str).value_counts().head(top_n)
    st.bar_chart(counts)
    st.dataframe(counts.rename("Frekuensi").rename_axis(selected_column).reset_index(), use_container_width=True)
else:
    st.info("Tidak ditemukan kolom teks/kategori untuk analisis frekuensi.")

st.subheader("Unduh data")
st.download_button(
    "Unduh data yang sedang dimuat (CSV)",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="spotify_playlists_copy.csv",
    mime="text/csv",
)

st.caption("Catatan: frekuensi kemunculan dalam dataset tidak otomatis berarti jumlah streaming atau popularitas global.")
