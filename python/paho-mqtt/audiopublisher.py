#!/usr/bin/python3

import asyncio
import random
import logging
import sys
import pyaudio
import functools
import struct
from mqttsubpub import MQTTPubSub

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def callback(mqttc, in_data, frame_count, time_info, flag):
    # audio_data = numpy.frombuffer(in_data, dtype=numpy.float32).tolist()
    audio_data = struct.unpack(frame_count * "h", in_data)
    print(frame_count, audio_data[0:16])
    # Snip out 512 values expand from [-1:1] to [0:1024]
    # Pack into {"time": "2021-01-01T12:00:00", "data": {"ACCX": [...]}}
    # Publish on "mls160a/0/v"

    mqttc.publish(
        'data',
        audio_data[0:16]
    )
    return (in_data, pyaudio.paContinue)


stream = None
audio_rate = 1024
buffer_size = 1024
paudio = pyaudio.PyAudio()
valid_rates = [1024, 2048, 4096, 32768, 65536, 48000, 44100]

def start(mqttc):
    global stream
    stop()
    stream = paudio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=audio_rate,
        frames_per_buffer=buffer_size,
        input=True,
        stream_callback=functools.partial(callback, mqttc),
    )


def stop():
    global stream
    if stream is not None:
        stream.stop_stream()
        stream.close()
        stream = None


async def main():
    queue = asyncio.Queue()  # Queue for incoming subscriptions
    death_event = asyncio.Queue()  # Queue for exiting

    with MQTTPubSub(
        lwt_topic='example/lwt',
        queue=queue,
    ) as mqttc:
        start(mqttc)

        tasks = []  # List of asyncio tasks

        # The following block adds an async command handler
        mqttc.subscribe('example/command')
        mqttc.subscribe('example/state/set')

        async def handle_command(queue):
            global audio_rate, buffer_size

            while True:
                message = await queue.get()
                logging.debug(message)

                if message['topic'] == 'example/state/set':
                    state = message['payload']
                    if state['value'] == 'dead':
                        logging.debug('DIE')
                        death_event.put_nowait('Your time has come')

                    if 'rate' in state and state['rate'].isdigit():
                        rate = int(state['rate'])
                        if rate in valid_rates:
                            audio_rate = rate
                            stop()
                    if 'bufsize' in state and state['bufsize'].isdigit():
                        bufsize = int(state['bufsize'])
                        if bufsize <= audio_rate:
                            buffer_size = bufsize
                            stop()

                if message['topic'] == 'example/command':
                    if message['payload']['value'] == 'start':
                        start(mqttc)
                    if message['payload']['value'] == 'stop':
                        stop()

                queue.task_done()

        tasks.append(asyncio.create_task(handle_command(queue)))

        # The following block adds an async status sender
        async def send_status():
            while True:
                mqttc.publish(
                    'example/state',
                    stream is None and "idle" or "streaming"
                )
                await asyncio.sleep(1)

        tasks.append(asyncio.create_task(send_status()))

        # Now wait for death to come.
        await death_event.get()

        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

        stop()
        paudio.terminate()


if __name__ == '__main__':
    asyncio.run(main())
