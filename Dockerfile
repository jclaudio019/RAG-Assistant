FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY knowledge/processed/chunks ./knowledge/processed/chunks
COPY knowledge/processed/vectors ./knowledge/processed/vectors
COPY evaluation ./evaluation

RUN pip install --no-cache-dir -e .

ENV PORT=8080
EXPOSE 8080

# GEMINI_API_KEY must be provided at runtime.
CMD ["python", "-m", "rag_assistant.main", "serve", "8080"]
