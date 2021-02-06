#!/usr/bin/python3

import asyncio
import random
import logging
import sys
from mqttsubpub import MQTTPubSub

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


async def main():
    queue = asyncio.Queue()

    with MQTTPubSub(
        base_topic='example',
        queue=queue,
    ) as mqttc:

        while mqttc.alive != 'dead':
            if mqttc.alive == 'on':
                mqttc.publish(
                    'random',
                    random.choice(['A', 'B', 'C'])
                )
            await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
