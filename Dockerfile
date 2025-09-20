FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt ./

# Install system dependencies + tzdata
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    python3-dev \
    tzdata \
 && rm -rf /var/lib/apt/lists/*

# Set timezone to UTC
ENV TZ=UTC

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run bot
CMD ["python3", "-m", "biisal"]
