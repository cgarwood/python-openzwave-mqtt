"""Emulate MQTT Broker with OZW Daemon instance from MQTT dump."""

# Experimental ! For debugging purposes
# This will host a MQTT (3.1.1) Broker on localhost:1883
# Content of the provided MQTT dump file will be published on the broker
# Setvalue command will be handled too.
# Connect with Hass + Z-Wave MQTT Addon and/or MQTT Explorer to test userdumps

# WARNING: Use dev version of HBMQTT pip install git+git://github.com/beerfactory/hbmqtt
# Use manual yaml config for mqtt in Hass, because Config flow seems to default to 3.1

import argparse
import asyncio
import json
import logging

from hbmqtt.broker import Broker
from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_0

BROKER_CONFIG = {
    "listeners": {
        "default": {"max-connections": 50000, "type": "tcp"},
        "my-tcp-1": {"bind": "127.0.0.1:1883"},
    },
    "timeout-disconnect-delay": 2,
    "auth": {"allow-anonymous": "true", "plugins": ["auth.anonymous"]},
    "topic-check": {"enabled": True, "plugins": ["topic_taboo"]},
}


def get_args():
    """Get arguments."""
    parser = argparse.ArgumentParser(description="OZW Emulator")
    parser.add_argument("filename", type=str, help="File with dump from mqtt.")
    return parser.parse_args()


async def publish_from_file():
    """Publish all topics from the provided dump file."""
    with open(dump_file, "rt") as fp:
        for line in fp:
            topic, payload = line.strip().split(",", 1)
            await mqtt_client.publish(topic, payload.encode(), retain=True)


async def process_messages():
    """Keep reading incoming messages from subscribed topics."""
    while True:
        msg = await mqtt_client.deliver_message()
        if not msg:
            continue
        topic = msg.topic
        data = msg.data.decode()
        if not data:
            continue
        data = json.loads(data)
        logging.info("Incoming message on topic %s --> %s", topic, data)
        if topic.endswith("/setvalue/"):
            value = data["Value"]
            if not isinstance(value, (int, float, bool)):
                logging.warning("setting this value is not supported")
                return
            # publish value in correct topic
            with open(dump_file, "rt") as fp:
                for line in fp:
                    value_topic, payload = line.strip().split(",", 1)
                    if value_topic.endswith(f'/value/{data["ValueIDKey"]}/'):
                        payload = json.loads(payload)
                        payload["Value"] = value
                        payload = json.dumps(payload).encode()
                        await mqtt_client.publish(value_topic, payload, retain=True)
                        break


if __name__ == "__main__":

    args = get_args()
    dump_file = args.filename
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    loop = asyncio.get_event_loop()

    # Run Broker
    broker = Broker(BROKER_CONFIG)
    loop.run_until_complete(broker.start())

    # Run Client
    mqtt_client = MQTTClient()
    loop.create_task(mqtt_client.connect("mqtt://localhost"))
    loop.create_task(publish_from_file())
    loop.create_task(mqtt_client.subscribe([("OpenZWave/1/command/#", QOS_0)]))
    loop.create_task(process_messages())

    loop.run_forever()
