# ESP8266 IoT Example
IoT data monitoring with MQTT, InfluxDB and Grafana using an ESP8266.

This repository contains a
[docker-compose](https://docs.docker.com/compose/) and
[Arduino ESP8266 (D1 Mini V3)](https://arduino-projekte.info/wemos-d1-mini-v3-0/)
based project for monitoring some real world sensor over a wifi network.

## A security note

These instructions do not explain how to secure your
MQTT or other communication with your server, e.g., with TLS.
The MQTT-Broker allows anonym connections - no user and password is needed to connect.

__Do NOT use this example in production!__

## Folders

- `docker`: Docker compose configuration for MQTT (Eclipse Mosquitto), InfluxDB, Grafana and a python script that receives MQTT data and stores them to InfluxDB
- `esp8266`: Arduino sketch file for the D1 Mini V3 that publishes sensor data via Wifi using MQTT

## Setup

### Cloning this repository

```sh
   git clone https://github.com/scharri/arduino-mqtt-example.git
   cd arduino-mqtt-example/docker
   docker-compose build
```

## Running MQTT, MQTTBridge, InfluxDB and Grafana

Run docker compose:

```sh
   cd arduino-mqtt-example/docker
   docker-compose up -d
```

This starts four containers: 
- mosquitto,
- influxdb, 
- grafana,
- mqttbridge

You can check that they are nicely up and running with

```sh
   docker ps
```

You should see all the four containers running continuously, and not restarting.
If any of them is restarting, you can use `docker logs <container-name>` to see its
logs.

To shut down your containers, e.g. if you need to change the settings, run
```sh
   docker-compose down
```

## Grafana setup
It is a good idea to log in your Grafana right away and change your
`admin` password.  You can also add an InfluxDB data source already now,
or later.  For having a meaningful Dashboard, you must first get some
data to your InfluxDB database.

- Access Grafana from `http://localhost:3000`
- Log in with user/password `admin/admin`
- Go to Configuration > Data Sources
- Add data source (InfluxDB)
  - Name: `InfluxDB`
  - URL: `http://influxdb:8086`
  - Database: `iot_db`
  - User: `root`
  - Password: `root`
  - Save & Test
- Create a Dashboard

## Programming the D1 Mini V3

For programming the D1 Mini V3, the easiest way is to use the
[Arduino IDE](https://www.arduino.cc/en/Main/Software).

D1 Mini V3 should send sensor data to the mosquitto broker to the following MQTT topic:
`iot/{device-identifier}/{sensorname}`.

For example: `iot/esp8266-example/temperature`.

Arduino sketch for the D1 Mini V3 is provided in `esp8266` folder.

Before flashing, you need to change the:
- `MQTT_BROKER_ADDR` constant to MQTT-Broker IP address,
- `WIFI_NAME` constant to Name of your Wifi,
- `WIFI_PASSWORD` constant to Password of your Wifi.