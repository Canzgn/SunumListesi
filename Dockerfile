# ---------- 1. Python imajını seç ----------
FROM python:3.12-slim

# ---------- 2. Sistem bağımlılıkları ----------
# psycopg2-binary derleme gerektirmez ama libpq lazım olabilir
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

# ---------- 3. Çalışma dizini ----------
WORKDIR /app

# ---------- 4. Pip bağımlılıkları (cache layer) ----------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- 5. Uygulama dosyalarını kopyala ----------
COPY . .

# ---------- 6. Upload klasörünü oluştur ----------
RUN mkdir -p static/uploads/kimlikler

# ---------- 7. Port ----------
EXPOSE 5001

# ---------- 8. Uygulamayı başlat ----------
CMD ["gunicorn", "run:app", "--workers", "4", "--timeout", "120", "--bind", "0.0.0.0:5001"]
