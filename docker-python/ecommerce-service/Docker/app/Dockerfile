# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.7-slim

ENV APP_HOME /app

WORKDIR $APP_HOME

# Copy files into the container image.
COPY . .

# Install dependencies.
RUN pip install -r requirements.txt

# Run the web service on container startup.
EXPOSE 8080