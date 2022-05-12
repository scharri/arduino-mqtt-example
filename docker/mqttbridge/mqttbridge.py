"""A MQTT to InfluxDB Bridge

This script receives MQTT data and saves those to InfluxDB.

"""

import re
from typing import NamedTuple
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import time

INFLUXDB_ADDRESS = 'influxdb'
INFLUXDB_USER = 'root'
INFLUXDB_PASSWORD = 'root'
INFLUXDB_DATABASE = 'iot_db'

MQTT_ADDRESS = 'mosquitto'
MQTT_TOPIC = 'iot/+/+'  # [device-identifier]/[temperature|humidity|heat_index|battery|status|...]
MQTT_REGEX = 'iot/([^/]+)/([^/]+)'
MQTT_CLIENT_ID = 'MQTTInfluxDBBridge'

class SensorData(NamedTuple):
    device_id: str
    measurement: str
    value: float
    
class MqttBridge():
    def __init__(self):
        print('Connecting to the database ' + INFLUXDB_DATABASE)
        self._influx_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)
        self._init_influxdb_database()
        self._mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
        self._mqtt_client.on_connect = self._on_connect
        self._mqtt_client.on_message = self._on_message
        self._mqtt_client.connect(MQTT_ADDRESS, 1883)

    def run(self):
        self._mqtt_client.loop_forever()

    def _on_connect(self, client, userdata, flags, rc):
        """ The callback for when the client receives a CONNACK response from the server."""
        print('Connected with result code ' + str(rc))
        client.subscribe(MQTT_TOPIC)


    def _on_message(self, client, userdata, msg):
        """The callback for when a PUBLISH message is received from the server."""
        print(msg.topic + ' ' + str(msg.payload))
        sensor_data = self._parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
        if sensor_data is not None:
            self._send_sensor_data_to_influxdb(sensor_data)


    def _parse_mqtt_message(self, topic, payload):
        match = re.match(MQTT_REGEX, topic)
        if match:
            device_id = match.group(1)
            measurement = match.group(2)
            return SensorData(device_id, measurement, float(payload))
        else:
            return None


    def _send_sensor_data_to_influxdb(self, sensor_data):
        json_body = [
            {
                'measurement': sensor_data.measurement,
                'tags': {
                    'device_id': sensor_data.device_id
                },
                'fields': {
                    'value': sensor_data.value
                }
            }
        ]
        self._influx_client.write_points(json_body)


    def _init_influxdb_database(self):
        databases = self._influx_client.get_list_database()
        if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
            print('Creating database ' + INFLUXDB_DATABASE)
            self._influx_client.create_database(INFLUXDB_DATABASE)
        self._influx_client.switch_database(INFLUXDB_DATABASE)


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge - IoT example')
    time.sleep(10)  # wait few seconds until the database is available
    mqttbridge = MqttBridge()
    mqttbridge.run()
    
