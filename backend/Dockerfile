FROM flyingjoe/uvicorn-gunicorn:python3.10-slim
LABEL maintainer="Ward Pearce <wardpearce@pm.me>"

COPY ./paaster /

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

ENV UVICORN_EXTRA_FLAGS="--proxy-headers"

COPY ./paaster/app /app
