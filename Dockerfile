FROM python:3.10

WORKDIR /webapps
ADD . /webapps

RUN mkdir -p /sd_image/

RUN pip3 install cmake
RUN pip3 install -r requirements.txt 
ENTRYPOINT python3 main.py

EXPOSE 8000