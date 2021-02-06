#!/usr/bin/python3

import time
import random
import logging
import sys
from mqttsubpub import MQTTPubSub

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


if __name__ == '__main__':
    with MQTTPubSub(
        base_topic='example'
    ) as mqttc:
        while mqttc.alive != 'dead':
            if mqttc.alive == 'on':
                mqttc.publish(
                    'random',
                    random.choice(['A', 'B', 'C'])
                )
            time.sleep(1)
