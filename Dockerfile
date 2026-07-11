# Base image python ka lightweight version
FROM python:3.10-slim

# Working directory set karein
WORKDIR /app

# Pehle requirements copy karein taaki Docker cache ka fayda mile
COPY requirements.txt .

# Dependencies install karein
RUN pip install --no-cache-dir -r requirements.txt

# Baaki ka application code copy karein
COPY app.py .

# Port expose karein
EXPOSE 5000

# App chalane ki command
CMD ["python", "app.py"]