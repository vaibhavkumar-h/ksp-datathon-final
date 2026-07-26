FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["sh", "-c", "python3 -m streamlit run login.py --server.port=${X_ZOHO_CATALYST_LISTEN_PORT:-8080} --server.address=0.0.0.0 --server.headless=true"]