FROM debian:jessie
RUN apt-get -y update && apt-get -y upgrade && apt-get -y install python3 python3-pip build-essential
RUN useradd -Um modron
USER modron
WORKDIR /home/modron

COPY modron ./modron
COPY setup.py .
RUN pip3 install --user .

ENTRYPOINT [".local/bin/modron"]
