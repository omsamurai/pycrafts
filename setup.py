from setuptools import setup, find_packages

setup(
    name = "pycrafts",
    version = "0.0.2",
    description = "Simple to code telegram bot",
    author = "Om",
    packages = find_packages(),
    install_requires=[
        "python-telegram-bot>=20.0",
        "python-dotenv>=1.0.0"
    ]
)