"""Provide an MQTT client for connecting to the ozwdaemon via MQTT broker."""
import asyncio
import json
import logging
import uuid
from contextlib import AsyncExitStack
from typing import Any, Callable, Dict, Optional, Set, Union

from asyncio_mqtt import Client as AsyncioClient, MqttError
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.subscribeoptions import SubscribeOptions

from openzwavemqtt import OZWManager, OZWOptions
from openzwavemqtt.const import LOGGER

PAHO_MQTT_LOGGER = logging.getLogger("paho.mqtt.client")
TOPIC_OPENZWAVE = "OpenZWave"


class MQTTClient:
    """Represent an MQTT client."""

    # pylint: disable=too-many-instance-attributes

    def __init__(
        self,
        host: str,
        port: int = 1883,
        **client_options: Any,
    ) -> None:
        """Set up client."""
        self.managers: Dict[int, OZWManager] = {}
        self.host = host
        self.port = port
        if "client_id" not in client_options:
            client_options["client_id"] = mqtt.base62(uuid.uuid4().int, padding=22)
        if "logger" not in client_options:
            client_options["logger"] = PAHO_MQTT_LOGGER
        self.client_options = client_options
        self.asyncio_client: AsyncioClient = None
        self.create_client()
        self.reconnect_interval = 1
        self.tasks: Set[asyncio.Task] = set()
        self.client_task: Optional[asyncio.Task] = None

    def create_client(self) -> None:
        """Create the asyncio client."""
        self.asyncio_client = AsyncioClient(
            self.host,
            self.port,
            **self.client_options,
        )

    async def connect(self, *, timeout: float = 10.0) -> None:
        """Connect to the broker.

        Can raise asyncio_mqtt.MqttError.
        """
        await self.asyncio_client.connect(timeout=timeout)

    async def disconnect(self, *, timeout: float = 10.0) -> None:
        """Disconnect from the broker.

        Can raise asyncio_mqtt.MqttError.
        """
        await self.asyncio_client.disconnect(timeout=timeout)

    async def publish(  # pylint:disable=too-many-arguments
        self,
        topic: str,
        payload: Optional[str] = None,
        qos: int = 0,
        retain: bool = False,
        properties: Optional[Properties] = None,
        timeout: float = 10,
    ) -> None:
        """Publish to topic.

        Can raise asyncio_mqtt.MqttError.
        """
        params: dict = {"qos": qos, "retain": retain, "timeout": timeout}
        if payload:
            params["payload"] = payload
        if properties:
            params["properties"] = properties

        LOGGER.debug("Sending message topic: %s, payload: %s", topic, payload)
        await self.asyncio_client.publish(topic, **params)

    async def subscribe(  # pylint:disable=too-many-arguments
        self,
        topic: str,
        qos: int = 0,
        options: Optional[SubscribeOptions] = None,
        properties: Optional[Properties] = None,
        timeout: float = 10.0,
    ) -> None:
        """Subscribe to topic.

        Can raise asyncio_mqtt.MqttError.
        """
        params: dict = {"qos": qos, "timeout": timeout}
        if options:
            params["options"] = options
        if properties:
            params["properties"] = properties

        await self.asyncio_client.subscribe(topic, **params)

    async def unsubscribe(
        self, topic: str, properties: Optional[Properties] = None, timeout: float = 10.0
    ) -> None:
        """Unsubscribe from topic.

        Can raise asyncio_mqtt.MqttError.
        """
        params: dict = {"timeout": timeout}
        if properties:
            params["properties"] = properties

        await self.asyncio_client.unsubscribe(topic, **params)

    async def safe_publish(self, *args: Any, **kwargs: Any) -> None:
        """Publish messages and catch MqttError."""
        try:
            await self.publish(*args, **kwargs)
        except MqttError as err:
            LOGGER.error("Failed sending message: %s", err)

    def add_manager(self, manager: OZWManager) -> None:
        """Add an OZW manager."""
        self.managers[id(manager)] = manager

    def send_message(self, topic: str, payload: Union[str, dict]) -> None:
        """Send a message from the manager options."""
        task = asyncio.create_task(self.safe_publish(topic, json.dumps(payload)))
        self.tasks.add(task)

    async def start_client(self) -> None:
        """Start the client."""
        self.client_task = asyncio.current_task()
        # Reconnect automatically until the client is stopped.
        while True:
            try:
                await self.subscribe_managers()
            except MqttError as err:
                self.reconnect_interval = min(self.reconnect_interval * 2, 900)
                LOGGER.error(
                    "MQTT error: %s. Reconnecting in %s seconds",
                    err,
                    self.reconnect_interval,
                )
                await asyncio.sleep(self.reconnect_interval)
                self.create_client()  # reset connect/reconnect futures

    async def subscribe_managers(self) -> None:
        """Connect and subscribe to manager topics."""
        async with AsyncExitStack() as stack:
            # Keep track of the asyncio tasks that we create, so that
            # we can cancel them on exit.
            tasks = self.tasks = set()
            stack.push_async_callback(cancel_tasks, tasks)

            # Connect to the MQTT broker.
            await stack.enter_async_context(self.asyncio_client)
            # Reset the reconnect interval after successful connection.
            self.reconnect_interval = 1

            # Messages that doesn't match a filter will get logged and handled here.
            messages = await stack.enter_async_context(
                self.asyncio_client.unfiltered_messages()
            )

            for manager in self.managers.values():
                task = asyncio.create_task(
                    handle_messages(messages, manager.receive_message)
                )
                tasks.add(task)

                # Note that we subscribe *after* starting the message loggers.
                # Otherwise, we may miss retained messages.
                topic = f"{manager.options.topic_prefix}#"
                await self.subscribe(topic)

            # Wait for everything to complete (or fail due to, e.g., network errors).
            # Make sure we await new tasks added while awaiting the first tasks.
            while self.tasks:
                current_tasks = list(self.tasks)
                self.tasks.clear()
                await asyncio.gather(*current_tasks)

    async def unsubscribe_manager(self, manager: OZWManager) -> None:
        """Unsubscribe the manager topic."""
        manager = self.managers[id(manager)]
        topic = f"{manager.options.topic_prefix}#"
        await self.unsubscribe(topic)

    async def remove_manager(self, manager: OZWManager) -> None:
        """Remove a manager."""
        manager_id = id(manager)
        manager = self.managers[manager_id]
        await self.unsubscribe_manager(manager)
        self.managers.pop(manager_id)
        if not self.managers:
            # Stop the client if there are no managers left.
            assert self.client_task is not None
            self.client_task.cancel()
            try:
                await self.client_task
            except asyncio.CancelledError:
                pass


async def handle_messages(messages: Any, callback: Callable[[str, str], None]) -> None:
    """Handle messages with callback."""
    async for message in messages:
        # Note that we assume that the message payload is an
        # UTF8-encoded string (hence the `bytes.decode` call).
        payload = message.payload.decode()
        LOGGER.debug("Received message topic: %s, payload: %s", message.topic, payload)
        callback(message.topic, payload)


async def cancel_tasks(tasks: Set[asyncio.Task]) -> None:
    """Cancel tasks."""
    for task in tasks:
        if task.done():
            continue
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


async def run_client() -> None:
    """Run client."""
    client = MQTTClient("localhost")
    options = OZWOptions(
        send_message=client.send_message, topic_prefix=f"{TOPIC_OPENZWAVE}/"
    )
    manager = OZWManager(options)
    client.add_manager(manager)

    await client.start_client()


def main() -> None:
    """Run main."""
    fmt = "%(asctime)s %(levelname)s (%(threadName)s) [%(name)s] %(message)s"
    logging.basicConfig(format=fmt, level=logging.DEBUG)
    LOGGER.info("Starting client.")

    try:
        asyncio.run(run_client())
    except KeyboardInterrupt:
        LOGGER.info("Exiting client.")


if __name__ == "__main__":
    main()
