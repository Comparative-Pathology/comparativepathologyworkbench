# Pull base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create directory for emails
RUN mkdir /Dummy

# create root directory for our project in the container
RUN mkdir /cpw

# Set the working directory to /music_service
WORKDIR /cpw

# Copy the current directory contents into the container at /music_service
ADD . /cpw/

# install psycopg2 dependencies
RUN apt-get update && apt-get -y install libpq-dev gcc && pip install psycopg2 && apt-get install -y iputils-ping

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .
