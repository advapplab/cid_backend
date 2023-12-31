FROM python:3.10

WORKDIR /webapps
ADD . /webapps

RUN mkdir -p /sd_image/
RUN mkdir -p /root/.insightface/models/
RUN wget -P /root/.insightface/models/ https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip 

RUN pip3 install cmake
RUN pip3 install -r requirements.txt 
# ENTRYPOINT python3 main.py
ENTRYPOINT gunicorn --certfile=cert.pem --keyfile=key.pem -b 0.0.0.0:8000 main:app --timeout 120

EXPOSE 8000
