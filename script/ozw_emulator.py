#!/usr/bin/env python3
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


def get_args() -> argparse.Namespace:
    """Get arguments."""
    parser = argparse.ArgumentParser(description="OZW Emulator")
    parser.add_argument("filename", type=str, help="File with dump from mqtt.")
    return parser.parse_args()


# pylint: disable=too-many-nested-blocks
async def process_messages(mqtt_client: MQTTClient, mqtt_data: dict) -> None:
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
        if topic.endswith("command/setvalue/"):
            new_value = data["Value"]
            for value_topic in mqtt_data:
                if not value_topic.endswith(f'/value/{data["ValueIDKey"]}/'):
                    continue
                payload = mqtt_data[value_topic]
                if isinstance(payload["Value"], dict):
                    payload["Value"]["Selected_id"] = new_value
                    # also update label
                    for item in payload["Value"]["List"]:
                        if item["Value"] == new_value:
                            payload["Value"]["Selected"] = item["Label"]
                            break
                elif isinstance(payload["Value"], (int, float, bool, str)):
                    payload["Value"] = new_value
                else:
                    logging.warning("setting this value type is not supported!")
                    return
                payload = json.dumps(payload).encode()
                await mqtt_client.publish(value_topic, payload, retain=True)
                break


async def emulate(args: argparse.Namespace) -> None:
    """Run broker and client and publish values."""

    # Parse data into a dict
    mqtt_data = {}
    with open(args.filename, "rt") as fp:
        for line in fp:
            item_topic, item_payload = line.strip().split(",", 1)
            mqtt_data[item_topic] = json.loads(item_payload)

    # Run Broker
    broker = Broker(BROKER_CONFIG)
    await broker.start()

    # Run Client
    client = MQTTClient()
    await client.connect("mqtt://localhost")

    # Publish all topics from the provided dump file
    for topic, data in mqtt_data.items():
        payload = json.dumps(data).encode()
        await client.publish(topic, payload, retain=True)

    # Subscribe to command topic and start listening for commands
    await client.subscribe([("OpenZWave/1/command/#", QOS_0)])
    try:
        await process_messages(client, mqtt_data)
    except asyncio.CancelledError:
        await client.disconnect()
        broker.shutdown()


def main() -> None:
    """Run main entrypoint."""
    args = get_args()
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)

    # Run
    try:
        asyncio.run(emulate(args))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
