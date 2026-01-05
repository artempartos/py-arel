FROM python:3.11-slim

WORKDIR /app

# Copy only requirements.txt first for layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Install project in development mode (if needed)
# RUN pip install -e .

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Run tests by default
CMD ["pytest", "tests/python", "-v"]
