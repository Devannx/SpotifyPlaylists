FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY deployment/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY deployment/ ./deployment/
COPY spotify_playlists.csv ./spotify_playlists.csv

EXPOSE 8501

CMD ["streamlit", "run", "deployment/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
