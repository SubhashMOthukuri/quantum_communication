from setuptools import setup, find_packages

setup(
    name="quantum_crypto",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask>=2.0.0",
        "cryptography>=44.0.0"
    ],
) 