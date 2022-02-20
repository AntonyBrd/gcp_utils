# Cloud Run and Fast API



Why Cloud Run instead of Cloud Compute Engine ?



## Dev in local

```sh
uvicorn main:app
```

## Tools 

Here is the list of tools and services I used during this project.

### Peotry for package management

Refer to official [Poetry Documentation](https://python-poetry.org/docs/basic-usage/).

```sh
# Create a new python app with poetry
poetry new <app-name>
# Add a dependency
poetry add <package-name>
# Use an existing project
poetry init
```

Start a web server with poetry. In ```pyproject.toml``` file, add the following lines:

```sh
[tool.poetry.scripts]
start = "<app-name>.main:start"
```

```sh
poetry run start
```


I noticed that unfortunately Poetry does not work on Cloud Run so I need to use a new Docker image.

Here is the old one :

```sh
FROM python:3.10.2-alpine3.15

LABEL maintainer="antony"

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.0.5


RUN apk add --no-cache gcc libffi-dev musl-dev

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /pocrapi
COPY poetry.lock pyproject.toml /pocrapi/

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /pocrapi

EXPOSE 8000

CMD poetry run start
```

poetry export -f requirements.txt --output requirements.txt


### Fast API

Refer te official [Fast API Documentation]()

### Cloud Run

Contenerize your app

**Local**

First and easy step, make it works in local using the [documentation](https://fastapi.tiangolo.com/deployment/docker/):

```sh
# Build image
docker build -t pocrapi:0.0.1 .
# Run server
docker run -d --name app1 -p 8000:8000 pocrapi:0.0.1
# Get IP (not needed)
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' app1
# now get on http://0.0.0.0:8000/weather is ok
# clean up
docker rm -f app1 
```

**On GCP**

Now try the following [tutorial](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service).


```sh
# Authenticate to Google Cloud Registry (gcr.io)
gcloud auth configure-docker

# Build & Push
docker build -t gcr.io/antony-brd/pocrapi:0.0.2 .
docker push gcr.io/antony-brd/pocrapi:0.0.2

# Deploy the loud Run service
gcloud run deploy pocrapi --image gcr.io/antony-brd/pocrapi:0.0.2 --platform managed --region europe-west4  --service-account godlike@antony-brd.iam.gserviceaccount.com --no-allow-unauthenticated

# Now deployed at https://pocrapi-ewhwlsvqqa-ez.a.run.app
curl -H "Content-Type: application/json" -d "access_token=$(gcloud auth application-default print-access-token)" https://pocrapi-ewhwlsvqqa-ez.a.run.apptokeninfo

# Make sure a service account can access the Cloud Run service
gcloud run services add-iam-policy-binding pocrapi --platform managed --region europe-west4 --member='serviceAccount:github-actions@antony-brd.iam.gserviceaccount.com'  --role=roles/run.invoker
gcloud run services add-iam-policy-binding pocrapi --platform managed --region europe-west4 --member='user:antonybernadou@gmail.com'  --role=roles/run.admin

# See if it has worked
gcloud run services get-iam-policy pocrapi --platform managed --region europe-west4

```
Attempt #2

Remove host and port in Dockerfile to match [this tutorial](https://cloud.google.com/run/docs/tutorials/secure-services), then:

```sh
# Build and push in one command 
gcloud builds submit --tag gcr.io/antony-brd/pocrapi:0.1.0

# Create an empty service account
gcloud iam service-accounts create pocrapi-account

# Deploy
gcloud run deploy pocrapi  --platform managed --region europe-west4  --image gcr.io/antony-brd/pocrapi:0.1.0  --service-account pocrapi-account   --no-allow-unauthenticated
```


* [Deploy a Flask app on Cloud Run](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service)
* [Better understanding of Cloud Run](https://github.com/ahmetb/cloud-run-faq)
* [FastAPI to Cloud Run example](https://github.com/anthonycorletti/cloudrun-fastapi/blob/main/Dockerfile)