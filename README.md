Python library for the OpenZWave MQTT implementation.

Consumes MQTT output from https://github.com/OpenZWave/qt-openzwave/blob/master/docs/MQTT.md

For Home Assistant integration, see the custom component [homeassistant-zwave_mqtt](https://github.com/cgarwood/homeassistant-zwave_mqtt).

## Structure

Each object maps to one or two parts in the topic. A topic can contain the following parts:

- `<Prefix>`: the prefix of each topic. This is ignored in the processing. Usually `openzwave/`.
- `<CollectionType>/<CollectionID>`: The collection type and the ID of the item in the collection. Example: `value/3`
- `<CollectionID>`: Some objects will have a direct collection that is not typed in the topic. Example is the OZW instance in `<Prefix>/1`
- `<ObjectType>`: If there is only a single instance of a type under a parent. For example `node/2/statistics`.

### Example

A message is sent to topic `openzwave/1/node/2/statistics`. This maps to:

| Type                | ID  |
| ------------------- | --- |
| Prefix              | -   |
| `OZWInstance`       | `1` |
| `OZWNode`           | `2` |
| `OZWNodeStatistics` | -   |

## Message ordering

We work with signals to signal listeners when things change. However, when we connect to MQTT we will receive a lot of retained messages at once. To prevent signals being sent out of order, we will hold all messages for children until the parent has received its information.

This has been disabled for `OZWManager` and `OZWInstance`.

If we receive messages on the following topics:

1. `openzwave/1/node/2/statistics`
2. `openzwave/1/node/2`

We will process the messages in the reverse order:

1. `openzwave/1/node/2`
2. `openzwave/1/node/2/statistics`

## Modelling Rules

This library should not aim to do fancy things. We should, as much as possible, represent the data from MQTT as-is. We don't want to change names besides making them Pythonic (CamelCase -> snake_case).

## Automatic added helpers

Models will have automatic helpers added based on their child models. For example, the `Node` model has the following child collections:

```python
    def create_collections(self):
        """Create collections that Node supports."""
        return {
            # A collection of children
            "instance": ItemCollection(OZWNodeInstance),
            # A single child
            "statistics": OZWNodeStatistics,
        }
```

This means that `Node` has the following automatic functions created:

- `get_instance(item_id)` to get an instance by ID.
- `instances()` to get an iterator over all available instances.
- `get_statistics()` get the direct child.

## Gathering Data

This library is instantiated using messages received from MQTT. To make development easier, we have created two helper scripts. One that will dump all MQTT messages and one that will read messages from a text file and instantiate an `OZWManager` with all the data. This can be used to develop, test or reproduce bugs.

```
python3 -m script.dump_mqtt > dump.csv
python3 -m script.instance_from_file dump.csv
```
