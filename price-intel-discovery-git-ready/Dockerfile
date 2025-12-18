FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN pip install -U pip

COPY pyproject.toml /app/
COPY src /app/src
COPY alembic.ini /app/
COPY alembic /app/alembic
COPY fixtures /app/fixtures
COPY README.md /app/

RUN pip install -e .

EXPOSE 8000
CMD ["bash", "-lc", "alembic upgrade head && uvicorn src.api.app:app --host 0.0.0.0 --port 8000"]
