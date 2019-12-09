# setuptools does not have type-stubs, so it's type errors are being ignored for now
from setuptools import setup  # type: ignore

setup(name="money", version="0.0.1", packages=["money"])
