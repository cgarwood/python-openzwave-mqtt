"""Setup module for python-openzwave-mqtt."""
from setuptools import find_packages, setup

VERSION = "0.0.6"


def readme():
    """Print long description."""
    with open("README.md") as f:
        return f.read()


setup(
    name="python-openzwave-mqtt",
    version=VERSION,
    url="https://github.com/cgarwood/python-openzwave-mqtt",
    download_url="https://github.com/cgarwood/python-openzwave-mqtt",
    author="Charles Garwood",
    author_email="cgarwood@gmail.com",
    description="Converts MQTT messages from qt-openzwave into Python objects and events",
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["*.tests"]),
    include_package_data=True,
    zip_safe=False,
    test_suite="tests",
)
