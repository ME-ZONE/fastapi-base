FROM python:3.10-bookworm

ENV APPLICATION_SERVICE=/app

# set work directory
RUN mkdir -p $APPLICATION_SERVICE

# where the code lives
WORKDIR $APPLICATION_SERVICE

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY pyproject.toml ./
RUN pip install --upgrade pip setuptools wheel && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry lock && \
    poetry install --only main --no-root

# copy project
COPY . $APPLICATION_SERVICE

CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 --timeout-keep-alive 300
