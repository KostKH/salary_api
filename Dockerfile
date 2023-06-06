FROM python:3.11-slim
RUN apt-get update && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.5.1 POETRY_HOME=/root/poetry python3 -
ENV PATH=$PATH:/root/poetry/bin \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
COPY poetry.lock pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
COPY ./salary_api/ ./salary_api/
WORKDIR /salary_api
CMD ["gunicorn","main:app","--workers","2","--worker-class","uvicorn.workers.UvicornWorker","--bind","0.0.0.0:8000"]

