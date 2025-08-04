FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /commonplace

ARG DEV=false

RUN if [ "$DEV" = "false" ]; then \
        apt-get update && apt-get install -y --no-install-recommends curl && \
        rm -rf /var/lib/apt/lists/* ; \
    else \
        apt-get update && apt-get install -y --no-install-recommends \
        build-essential git && \
        rm -rf /var/lib/apt/lists/* ; \
    fi

COPY requirements.in requirements_dev.in ./

RUN pip install --upgrade pip pip-tools

RUN if [ "$DEV" = "false" ]; then \
        pip-compile requirements.in && pip install -r requirements.txt ; \
    else \
        pip-compile requirements_dev.in && pip install -r requirements_dev.txt ; \
    fi

COPY . /commonplace/

RUN if [ "$DEV" = "false" ]; then \
        pyhon manage.py collectstatic --noinput ; \
    fi
