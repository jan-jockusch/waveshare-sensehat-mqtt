import paho.mqtt.client
import json
import json.decoder
import logging
import time


class MQTTPubSub:
    '''Publisher and Subscriber class which makes building simple MQTT
    clients easier.

    This class enforces using UTF-8 encoded JSON as the payload.
    TODO: Perhaps this mandatory conversion is too strict and should be
    optional.
    '''

    def __init__(self, hostname='localhost', port=1883, queue=None,
                 lwt_topic=None, lwt_payload='lwt'):
        self.hostname = hostname
        self.port = port
        self.queue = queue
        self.lwt_topic = lwt_topic
        self.lwt_payload = lwt_payload

        self.is_connected = False
        self.client = paho.mqtt.client.Client()
        if self.lwt_topic:
            self.client.will_set(
                topic=self.lwt_topic,
                payload=self.lwt_payload,
                retain=True,
            )
        self.client.user_data_set(self)
        self.client.on_connect = MQTTPubSub.on_connect
        self.client.on_message = MQTTPubSub.on_message
        logging.info("Init complete")

    def connect(self):
        self.client.connect(self.hostname, self.port, 60)
        self.client.loop_start()
        # Wait for connect
        while not self.is_connected:
            time.sleep(0.1)
        logging.info("Connected")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        logging.info("Disconnect done")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        if rc != 0:
            logging.error("Connection refused, error code " + repr(rc))
            raise ValueError("Connection refused")
        userdata.is_connected = True
        logging.info("Connected")

    @staticmethod
    def on_message(client, userdata, msg):
        try:
            payload_decoded = msg.payload.decode('utf-8')
        except UnicodeDecodeError:
            logging.info("Non-UTF-8 string found. Using binary value")
            payload = msg.payload
        else:
            try:
                payload = json.loads(payload_decoded)
            except json.decoder.JSONDecodeError:
                logging.info("Invalid JSON found. Using string value")
                payload = payload_decoded

        if not isinstance(payload, dict):
            payload = {
                'value': payload,
            }
        logging.debug("Message received: {} = {}".format(msg.topic, payload))

        # Place the message into the given queue to allow processing in the
        # main loop
        if userdata.queue is not None:
            userdata.queue.put_nowait({
                'topic': msg.topic,
                'payload': payload,
            })
        return

    def publish(self, topic, payload, retain=False, qos=0):
        '''Publishing wrapper which automatically encodes the data structure
        in a compliant way.
        '''
        self.client.publish(
            topic=topic,
            payload=json.dumps(payload).encode('utf-8'),
            retain=retain,
            qos=qos,
        )

    def subscribe(self, topic):
        '''Simple subscribe wrapper just to shorten calls.
        '''
        self.client.subscribe(topic)
