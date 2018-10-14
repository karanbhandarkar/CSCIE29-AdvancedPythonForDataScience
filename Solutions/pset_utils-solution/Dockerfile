FROM python:3.6 AS base

ENV PIP_NO_CACHE_DIR off
ENV PYTHONPATH="/app:${PYTHONPATH}";

# RUN will execute any commands in a new layer on top of the current image 
# and commit the results 
RUN pip install pipenv 

WORKDIR /app

# RUN will execute any commands in a new layer on top of the current image 
# and commit the results 
RUN pipenv install

# copy/add Pipfile and Pipefile.local from local file system to image CWD
COPY Pipfile .
COPY Pipfile.lock .

# RUN will execute any commands in a new layer on top of the current image 
# and commit the results 
RUN pipenv install --system --dev
