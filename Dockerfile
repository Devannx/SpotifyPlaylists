
# Menggunakan image Python
FROM python:3.11-slim

# Menentukan direktori kerja
WORKDIR /app

# Menyalin file proyek ke container
COPY . /app

# Menginstal library yang dibutuhkan
RUN pip install --no-cache-dir \
    pandas \
    numpy \
    matplotlib \
    seaborn \
    scikit-learn \
    jupyter

# Membuka port Jupyter Notebook
EXPOSE 8888

# Menjalankan Jupyter Notebook
CMD ["jupyter", "notebook", \
     "--ip=0.0.0.0", \
     "--port=8888", \
     "--no-browser", \
     "--allow-root", \
     "--ServerApp.token="]
