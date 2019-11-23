import argparse
import logging

from threading import Timer

try:
    import paho.mqtt.client as mqtt
except ImportError:
    mqtt = None


def get_args():
    parser = argparse.ArgumentParser(description="Dump Instance")
    parser.add_argument(
        "--host", type=str, default="localhost", help="Host of the MQTT server.",
    )
    parser.add_argument(
        "--port", type=int, default=1883, help="Port that the MQTT server runs on.",
    )
    return parser.parse_args()


def main():
    args = get_args()
    mqttc = mqtt.Client()
    mqttc.enable_logger(logging.getLogger("dump_instance"))
    mqttc.on_message = lambda _client, _userdata, msg: print(
        f"{msg.topic},{msg.payload.decode()}"
    )

    mqttc.connect(args.host, args.port, 60)
    mqttc.subscribe("openzwave/#", 0)

    # Give it two seconds to receive all messages before we disconnect.
    Timer(2, mqttc.disconnect).start()

    mqttc.loop_forever()


if __name__ == "__main__":
    if mqtt is None:
        print("Please install paho-mqtt to use this script.")
        print("python3 -m pip install paho-mqtt")
    else:
        main()
