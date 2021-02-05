#!/usr/bin/python3

import paho.mqtt.client
import json
import time
import random


class MQTTSender(paho.mqtt.client.Client):

    def __enter__(self):
        self.will_set('machine/1/alive', json.dumps("0"), retain=True)
        self.connect('127.0.0.1', 1883, 60)
        self.loop_start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.loop_stop()

    def on_connect(self, obj, flags, rc):
        self.publish('machine/1/alive', json.dumps("1"), retain=True)

    def run(self):
        self.publish(
            'machine/1/state',
            json.dumps(random.choice(['A', 'B', 'C']))
        )


if __name__ == '__main__':
    with MQTTSender() as mqttc:
        for round in range(100):
            mqttc.run()
            time.sleep(1)
