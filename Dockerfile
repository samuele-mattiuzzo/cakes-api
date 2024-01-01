# python version and image
FROM python:3.11.5-slim-bullseye

# setup env variables  
ENV DockerHOME=/home/app/webapp  

# set work directory  
RUN mkdir -p $DockerHOME 
WORKDIR $DockerHOME  

# set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# install dependencies  
RUN pip install --upgrade pip  

# copy the project
COPY . $DockerHOME  
# install dependencies
RUN pip install -r requirements.txt  
