# Gunakan base image Python 3.11
FROM python:3.11-slim

# Set working directory di container
WORKDIR /app

# Salin file requirements.txt dan install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file aplikasi ke container
COPY . .

# Expose port sesuai aplikasi (Flask default 5000)
EXPOSE 5000

# Environment variable untuk Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Jalankan aplikasi Flask
CMD ["flask", "run"]
