
FROM python:3.11-slim

WORKDIR /usr/src/app

# Install minimal build tools for scikit-learn
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
# This step will now be much faster (minutes, not hours)
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]