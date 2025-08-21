FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy project specification and install dependencies first (leverages Docker cache)
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Copy the remaining project files (if any)
COPY expenses_data.json ./

EXPOSE 8501

CMD ["streamlit", "run", "-m", "homesplit.app", "--server.port", "8501", "--server.address", "0.0.0.0"]