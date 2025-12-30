# 1. Use lightweight Python image
FROM python:3.11-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Copy requirements first (Docker cache optimization)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy Streamlit app code
COPY . .

# 6. Expose Streamlit port
EXPOSE 8501

# 7. Run Streamlit
CMD ["streamlit", "run", "index.py", "--server.address=0.0.0.0", "--server.port=8501"]
