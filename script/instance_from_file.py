import argparse

import openzwavemqtt


def get_args():
    parser = argparse.ArgumentParser(description="Dump Instance")
    parser.add_argument(
        "filename", type=str, help="File with messages to process.",
    )
    return parser.parse_args()


def main():
    args = get_args()
    mgr = openzwavemqtt.OZWManager(openzwavemqtt.OZWOptions(None))
    with open(args.filename, "rt") as fp:
        for line in fp:
            topic, payload = line.strip().split(",", 1)
            try:
                mgr.receive_message(topic, payload)
            except ValueError:
                print(f"Unable to process message on topic {topic} as JSON")
                print(payload)
                return


if __name__ == "__main__":
    main()
