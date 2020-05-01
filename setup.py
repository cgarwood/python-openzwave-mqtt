"""Setup module for python-openzwave-mqtt."""
from pathlib import Path

from setuptools import find_packages, setup

PROJECT_DIR = Path(__file__).parent.resolve()
README_FILE = PROJECT_DIR / "README.md"
VERSION = "1.0.0"


setup(
    name="python-openzwave-mqtt",
    version=VERSION,
    url="https://github.com/cgarwood/python-openzwave-mqtt",
    download_url="https://github.com/cgarwood/python-openzwave-mqtt",
    author="Charles Garwood",
    author_email="cgarwood@gmail.com",
    description="Converts MQTT messages from qt-openzwave into Python objects and events",
    long_description=README_FILE.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["test.*", "test"]),
    python_requires=">=3.7",
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Home Automation",
    ],
)
