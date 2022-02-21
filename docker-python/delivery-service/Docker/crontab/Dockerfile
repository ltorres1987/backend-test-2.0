FROM python:3.7-slim

ENV APP_HOME /app

WORKDIR $APP_HOME

# Copy files into the container image.
COPY . .

RUN apt-get update && apt-get -y install cron vim

# Install dependencies.
RUN pip install -r requirements.txt

COPY crontab /etc/cron.d/crontab

RUN chmod 0644 /etc/cron.d/crontab

RUN /usr/bin/crontab /etc/cron.d/crontab

RUN echo $PYTHONPATH

# run crond as main process of container
CMD ["cron", "-f"]