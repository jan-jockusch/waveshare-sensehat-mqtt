import paho.mqtt.client
import json
import json.decoder
import logging


class MQTTPubSub:
    '''Publisher and Subscriber class which makes building simple MQTT
    clients easier.
    '''

    def __init__(self, hostname='localhost', port=1883, base_topic='example',
                 state_topic='state'):
        self.hostname = hostname
        self.port = port
        self.base_topic = base_topic
        self.state_topic = state_topic

        self.is_alive = 'dead'
        self.client = paho.mqtt.client.Client()
        self.client.will_set(
            topic=self.base_topic + '/' + self.state_topic,
            payload=json.dumps(self.is_alive),
            retain=True,
        )
        self.client.user_data_set(self)
        self.client.on_connect = MQTTPubSub.on_connect
        self.client.on_message = MQTTPubSub.on_message
        self.client.connect(self.hostname, self.port, 60)
        self.client.loop_start()
        self.alive = 'on'
        logging.info("Init complete")

    @property
    def alive(self):
        return self.is_alive

    @alive.setter
    def alive(self, status):
        self.is_alive = status
        self.client.publish(
            topic=(self.base_topic + '/' + self.state_topic),
            payload=json.dumps(self.is_alive),
            retain=True,
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.alive = 'dead'
        self.client.loop_stop()
        self.client.disconnect()
        logging.info("Disconnect done")

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        client.subscribe(
            userdata.base_topic + '/' + userdata.state_topic + '/set')
        logging.info("Connected")

    @staticmethod
    def on_message(client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
        except json.decoder.JSONDecodeError:
            logging.exception("Message needs to be valid JSON")
            return
        except UnicodeDecodeError:
            logging.exception("Message needs to be UTF-8 encoded")
            return
        if not isinstance(payload, dict):
            payload = {
                'value': payload,
            }
        logging.debug("Message received: {} = {}".format(msg.topic, payload))

        if not isinstance(payload['value'], str):
            logging.error("Rejecting value because it is not a string.")
            return
        if payload['value'] not in ('dead', 'on', 'off'):
            logging.error("Invalid state. Must be dead, on, or off")
            return
        userdata.alive = payload['value']
        return

    def publish(self, subtopic, json_payload):
        '''Publishing wrapper which automatically encodes the data structure
        in a compliant way.
        '''
        self.client.publish(
            topic=self.base_topic + '/' + subtopic,
            payload=json.dumps(json_payload).encode('utf-8'),
            retain=False,
            qos=0,
        )
