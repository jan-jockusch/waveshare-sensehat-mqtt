#!/usr/bin/python3

import asyncio
import random
import logging
import sys
from mqttsubpub import MQTTPubSub

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


async def main():
    queue = asyncio.Queue()  # Queue for incoming subscriptions
    death_event = asyncio.Queue()  # Queue for exiting

    with MQTTPubSub(
        lwt_topic='example/lwt',
        queue=queue,
    ) as mqttc:

        tasks = []  # List of asyncio tasks

        # The following block adds an async command handler
        mqttc.subscribe('example/command')
        mqttc.subscribe('example/state/set')

        async def handle_command(queue):
            while True:
                message = await queue.get()
                print(message)

                if message['topic'] == 'example/state/set':
                    if message['payload']['value'] == 'dead':
                        death_event.put_nowait('Your time has come')

                queue.task_done()

        tasks.append(asyncio.create_task(handle_command(queue)))

        # The following block adds an async status sender
        async def send_status():
            while True:
                mqttc.publish(
                    'random',
                    random.choice(['A', 'B', 'C'])
                )
                await asyncio.sleep(1)

        tasks.append(asyncio.create_task(send_status()))

        # Now wait for death to come.
        await death_event.get()

        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == '__main__':
    asyncio.run(main())
