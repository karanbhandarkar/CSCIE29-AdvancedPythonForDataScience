FROM python:3.6 AS base

ARG CI_USER_TOKEN
RUN echo "machine github.com\n login $CI_USER_TOKEN\n" > ~/.netrc

# RUN will execute any commands in a new layer on top of the current image 
# and commit the results
RUN pip install pipenv 

ENV \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  PIPENV_HIDE_EMOJIS=true \
  PIPENV_COLORBLIND=true \
  PIPENV_NOSPIN=true \
  PYTHONPATH="/app:${PYTHONPATH}"

# switch to /build in image
WORKDIR /build

RUN pipenv install

# copy/add Pipfile and Pipefile.local from local file system to image CWD
COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --system --deploy --ignore-pipfile --dev
#switch to /app in image
WORKDIR /app
