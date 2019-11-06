from setuptools import setup

setup(
    name="python-openzwave-mqtt",
    version="0.0.1",
    url="https://github.com/cgarwood/python-openzwave-mqtt",
    download_url="https://github.com/cgarwood/python-openzwave-mqtt",
    author="Charles Garwood",
    author_email="cgarwood@gmail.com",
    packages=["openzwavemqtt"],
    include_package_data=True,
    zip_safe=False,
    test_suite="tests",
    install_requies=["attr"],
)
