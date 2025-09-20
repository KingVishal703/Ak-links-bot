FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt ./

# Install system dependencies + tzdata
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    python3-dev \
    tzdata \
 && rm -rf /var/lib/apt/lists/*

# Set timezone to UTC
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Ensure Python unbuffered logs
ENV PYTHONUNBUFFERED=1

# Run bot
CMD ["python3", "-m", "biisal"]
