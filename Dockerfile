FROM python:3.9-slim

# Install system dependencies needed for OpenCV and headless graphics
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu && \
    pip install -r requirements.txt

# Copy the rest of the application files
COPY . .

# Set default port for Hugging Face Spaces (can be overridden by Render/Railway environment)
ENV PORT=7860
EXPOSE 7860

# Shell form of CMD to expand the dynamic $PORT environment variable
CMD gunicorn --bind 0.0.0.0:$PORT app:app
