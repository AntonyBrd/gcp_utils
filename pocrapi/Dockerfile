FROM python:3.10.2-alpine3.15

LABEL maintainer="antony"

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 

RUN apk add --no-cache gcc libffi-dev musl-dev

WORKDIR /pocrapi

COPY . /pocrapi

RUN pip install -r requirements.txt

CMD uvicorn pocrapi.main:app --fd $PORT --workers 1 --proxy-headers
