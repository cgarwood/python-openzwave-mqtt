"""Provide an MQTT client for connecting to the ozwdaemon via MQTT broker."""
import asyncio
import json
import logging
from contextlib import AsyncExitStack
from typing import Any, Callable, Optional, Set, Union

from asyncio_mqtt import Client as AsyncioClient, MqttError
from paho.mqtt.properties import Properties
from paho.mqtt.subscribeoptions import SubscribeOptions

from openzwavemqtt import OZWManager, OZWOptions
from openzwavemqtt.const import LOGGER

TOPIC_OPENZWAVE = "OpenZWave"


class MQTTClient:
    """Represent an MQTT client."""

    def __init__(
        self,
        host: str,
        port: int = 1883,
        **client_options: Any,
    ) -> None:
        """Set up client."""
        self.manager: Optional[OZWManager] = None
        self.host = host
        self.port = port
        self.client_options = client_options
        self.asyncio_client: AsyncioClient = None
        self.create_client()
        self.reconnect_interval = 1
        self.tasks: Set[asyncio.Task] = set()

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
        self.manager = manager

    def send_message(self, topic: str, payload: Union[str, dict]) -> None:
        """Send a message from the manager options."""
        task = asyncio.create_task(self.safe_publish(topic, json.dumps(payload)))
        self.tasks.add(task)

    async def start_client(self) -> None:
        """Start the client."""
        # Reconnect automatically until the client is stopped.
        while True:
            try:
                await self.connect_subscribe()
            except MqttError as err:
                self.reconnect_interval = min(self.reconnect_interval * 2, 900)
                LOGGER.error(
                    "MQTT error: %s. Reconnecting in %s seconds",
                    err,
                    self.reconnect_interval,
                )
                await asyncio.sleep(self.reconnect_interval)
                self.create_client()  # reset connect/reconnect futures

    async def connect_subscribe(self) -> None:
        """Connect and subscribe to topic."""
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
            assert self.manager is not None
            task = asyncio.create_task(
                handle_messages(messages, self.manager.receive_message)
            )
            tasks.add(task)

            # Note that we subscribe *after* starting the message loggers.
            # Otherwise, we may miss retained messages.
            topic = f"{self.manager.options.topic_prefix}#"
            await self.subscribe(topic)

            # Wait for everything to complete (or fail due to, e.g., network errors).
            # Make sure we await new tasks added while awaiting the first tasks.
            while self.tasks:
                current_tasks = list(self.tasks)
                self.tasks.clear()
                await asyncio.gather(*current_tasks)


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
