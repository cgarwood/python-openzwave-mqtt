#!/usr/bin/env python3
"""Dump mqtt output."""
import argparse
import logging
from threading import Timer
from typing import Any

try:
    import paho.mqtt.client as mqtt
except ImportError:
    mqtt = None


def get_args() -> argparse.Namespace:
    """Get arguments."""
    parser = argparse.ArgumentParser(description="Dump Instance")
    parser.add_argument(
        "--host", type=str, default="localhost", help="Host of the MQTT server."
    )
    parser.add_argument(
        "--port", type=int, default=1883, help="Port that the MQTT server runs on."
    )
    return parser.parse_args()


def main() -> None:
    """Run main entrypoint."""
    args = get_args()
    mqttc = mqtt.Client()
    mqttc.enable_logger(logging.getLogger("dump_instance"))

    def print_message(
        _client: mqtt.Client, _userdata: Any, msg: mqtt.MQTTMessage
    ) -> None:
        """Print message."""
        payload = msg.payload.decode().replace("\n", "")
        print(f"{msg.topic},{payload}")

    mqttc.on_message = print_message

    mqttc.connect(args.host, args.port, 60)
    mqttc.subscribe("OpenZWave/#", 0)

    # Give it two seconds to receive all messages before we disconnect.
    Timer(2, mqttc.disconnect).start()

    mqttc.loop_forever()


if __name__ == "__main__":
    if mqtt is None:
        print("Please install paho-mqtt to use this script.")
        print("python3 -m pip install paho-mqtt")
    else:
        main()
