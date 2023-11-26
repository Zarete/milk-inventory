FROM python:3.11-slim

WORKDIR /home/app

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev --no-interaction

COPY . .

ENTRYPOINT ["poetry", "run", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]