FROM python:3.11

RUN mkdir /app

WORKDIR /app

COPY pyproject.toml .

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY .. .

RUN chmod a+x scripts/*.sh
