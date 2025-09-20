FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt ./

# Install system deps + tzdata + ntp
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    python3-dev \
    tzdata \
    ntpdate \
 && rm -rf /var/lib/apt/lists/*

# Force timezone UTC
ENV TZ=UTC

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Sync time before starting bot
CMD ntpdate -u pool.ntp.org && python3 -m biisal
