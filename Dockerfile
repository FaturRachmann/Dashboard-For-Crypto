# Gunakan base image Python 3.11
FROM python:3.11-slim

# Set working directory di container
WORKDIR /app

# Salin file requirements.txt dan install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file aplikasi
COPY . .

# Expose port default Streamlit
EXPOSE 8501

# Jalankan Streamlit
CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
