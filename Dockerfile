ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install -U --no-cache-dir poetry pip && poetry config virtualenvs.create false

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry install --no-interaction --no-ansi --no-root --without dev

COPY .env .env
COPY ./bakery ./bakery

EXPOSE 8000

ENV APP_WORKERS=1

CMD ["python", "-m", "bakery"]