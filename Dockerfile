FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry
RUN poetry install

COPY . /app

CMD ["uvicorn", "dop_zhu_zad.main:app", "--host", "0.0.0.0", "--port", "8000"]
