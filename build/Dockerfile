FROM python:3.11

# Define environment vars to expose to container here
# ENV <key> <value>

# Env vars sent from docker-compose or docker build
ARG uid=1000
ARG gid=1000

RUN getent group $gid || groupadd --gid $gid steam-hardware-survey
RUN getent passwd $uid || useradd -m -u $uid -g $gid steam-hardware-survey

RUN chown -R $uid:$gid /usr/local

RUN apt-get update -y \
  && rm -rf /var/lib/apt/lists/*

USER $uid

COPY requirements.txt /code/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt
