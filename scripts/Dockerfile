FROM ubuntu:20.04

RUN apt update -y && apt install -y wget vim python3 python3-distutils  git
RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py
WORKDIR /dragonfly
ADD . .
#RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install virtualenv
