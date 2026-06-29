FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

ENV URL="https://homoapi.bancocoinag.com"
ENV MONGO="mongodb://admin:Fidelius2025*@10.158.0.29:27018/"
ENV MONGODB_DB='coinag'

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
