FROM python:3.9-slim

# copy requirements files
WORKDIR /app
COPY ./pyproject.toml ./poetry.lock /app/

# generate requirements.txt using poetry
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry export -f requirements.txt --output requirements.txt

# set up service account
RUN useradd -ms /bin/bash service
USER service

# allow the package repo URL to be passed in as an arg
ARG PACKAGE_REPO_URL

# install requirements
RUN pip install -r requirements.txt --extra-index-url $PACKAGE_REPO_URL

# copy the rest of the source code
COPY . /app

# run uvicorn
CMD poetry show
# FIXME: run CMD here...


