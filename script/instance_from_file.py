#!/usr/bin/env python3
"""Create an instance from a file with dumped mqtt messages."""
import argparse
import re
from typing import Optional, Set, Tuple

import openzwavemqtt
from openzwavemqtt import base


class ExitException(Exception):
    """Represent an exit error."""


def get_args() -> argparse.Namespace:
    """Get arguments."""
    parser = argparse.ArgumentParser(description="Dump Instance")
    parser.add_argument(
        "filename", type=str, help="File with messages to process.",
    )
    return parser.parse_args()


def load_mgr_from_file(mgr: openzwavemqtt.OZWManager, file_path: str) -> None:
    """Load manager from file."""
    with open(file_path, "rt") as fp:
        for line in fp:
            topic, payload = line.strip().split(",", 1)
            try:
                mgr.receive_message(topic, payload)
            except ValueError:
                raise ExitException(
                    f"Unable to process message on topic {topic} as JSON: {payload}"
                )


def camelcase_to_snake_case(name: str) -> str:
    """Convert camelCase to snake_case."""
    # Otherwise ZWave -> _z_wave_ in names.
    name = (
        name.replace("ZWave", "Zwave")
        .replace("OpenZwave", "Openzwave")
        .replace("_", "")
    )
    s_1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s_1).lower()


def verify_integrity(
    model: base.ZWaveBase, warned: Optional[Set[Tuple[str, str]]] = None
) -> None:
    """Verify the integrity of the loaded data."""
    if warned is None:
        warned = set()

    model_name = type(model).__name__
    obj_name = f"{model_name}/{model.id}"

    if model.pending_messages is not None:
        print(f"{obj_name} has pending messages!")

    if model.data is not None and model.data != model.DEFAULT_VALUE:
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
        if isinstance(model_or_collection, base.ZWaveBase):
            verify_integrity(model_or_collection, warned)
            continue

        if isinstance(model_or_collection, base.ItemCollection):
            for model_ in model_or_collection.collection.values():
                verify_integrity(model_, warned)


def main() -> None:
    """Run main entrypoint."""
    args = get_args()
    mgr = openzwavemqtt.OZWManager(openzwavemqtt.OZWOptions(print))
    load_mgr_from_file(mgr, args.filename)
    verify_integrity(mgr)


if __name__ == "__main__":
    try:
        main()
    except ExitException as err:
        print(f"Fatal error: {err}")
