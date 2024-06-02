FROM python:3.11

RUN mkdir code

WORKDIR /code

COPY /pyproject.toml /code

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .