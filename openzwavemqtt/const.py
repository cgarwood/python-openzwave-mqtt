import logging

LOGGER = logging.getLogger("openzwavemqtt")

EVENT_PLACEHOLDER = "missing"

EVENT_COMMAND_CLASS_ADDED = "command_class_added"
EVENT_COMMAND_CLASS_CHANGED = "command_class_changed"
EVENT_COMMAND_CLASS_REMOVED = "command_class_removed"

EVENT_INSTANCE_ADDED = "instance_added"
EVENT_INSTANCE_CHANGED = "instance_changed"
EVENT_INSTANCE_REMOVED = "instance_removed"

EVENT_INSTANCE_STATISTICS_CHANGED = "instance_statistics_changed"
EVENT_INSTANCE_STATUS_CHANGED = "instance_status_changed"

EVENT_NODE_ADDED = "node_added"
EVENT_NODE_CHANGED = "node_changed"
EVENT_NODE_REMOVED = "node_removed"
EVENT_NODE_INSTANCE_ADDED = "node_instance_added"
EVENT_NODE_INSTANCE_CHANGED = "node_instance_changed"
EVENT_NODE_INSTANCE_REMOVED = "node_instance_removed"
EVENT_NODE_STATISTICS_CHANGED = "node_statistics_changed"

EVENT_VALUE_ADDED = "value_added"
EVENT_VALUE_CHANGED = "value_changed"
EVENT_VALUE_REMOVED = "value_removed"

EMPTY = {}
