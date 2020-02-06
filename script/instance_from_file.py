import argparse
import re

import openzwavemqtt
from openzwavemqtt.base import ZWaveBase


class ExitException(Exception):
    pass


def get_args():
    parser = argparse.ArgumentParser(description="Dump Instance")
    parser.add_argument(
        "filename", type=str, help="File with messages to process.",
    )
    return parser.parse_args()


def load_mgr_from_file(mgr: openzwavemqtt.OZWManager, file_path):
    with open(file_path, "rt") as fp:
        for line in fp:
            topic, payload = line.strip().split(",", 1)
            try:
                mgr.receive_message(topic, payload)
            except ValueError:
                raise ExitException(
                    f"Unable to process message on topic {topic} as JSON: {payload}"
                )


def camelcase_to_snake_case(name):
    # Otherwise ZWave -> _z_wave_ in names.
    name = name.replace("ZWave", "Zwave")
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def verify_integrity(model: ZWaveBase, warned=None):
    if warned is None:
        warned = set()

    model_name = type(model).__name__
    obj_name = f"{model_name}/{model.id}"

    if model.pending_messages is not None:
        print(f"{obj_name} has pending messages!")

    if model.data != model.DEFAULT_VALUE:
        for key, value in model.data.items():
            prop_name = camelcase_to_snake_case(key)

            if (model_name, key) in warned:
                continue

            if hasattr(model, prop_name):
                continue

            print(
                f"""

    # {model_name}

    @property
    def {prop_name}(self) -> {type(value).__name__}:
        \"\"\"Return {key}.\"\"\"
        return self.data.get("{key}")

"""
            )
            warned.add((model_name, key))

    # Process children
    for model_or_collection in model.collections.values():
        if isinstance(model_or_collection, ZWaveBase):
            verify_integrity(model_or_collection, warned)
            continue

        for model in model_or_collection.collection.values():
            verify_integrity(model, warned)


def main():
    args = get_args()
    mgr = openzwavemqtt.OZWManager(openzwavemqtt.OZWOptions(None))
    load_mgr_from_file(mgr, args.filename)
    verify_integrity(mgr)


if __name__ == "__main__":
    try:
        main()
    except ExitException as err:
        print(f"Fatal error: {err}")
