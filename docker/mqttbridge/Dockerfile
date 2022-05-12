FROM python:3.10.4-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY mqttbridge.py .


CMD ["python3", "-u", "mqttbridge.py"]
