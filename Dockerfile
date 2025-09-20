FROM python:3.9-alpine

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt ./

# Install build tools and timezone
RUN apk add --no-cache build-base gcc musl-dev linux-headers tzdata

# Set timezone to UTC (fixes Pyrogram BadMsgNotification)
ENV TZ=UTC

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run bot
CMD ["python3", "-m", "biisal"]
