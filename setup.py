import setuptools

setuptools.setup(
    name="peaqevcore",
    version="0.0.5",
    author="Magnus Eldén",
    description="Core types for peaqev car charging",
    packages=["peaqevcore"],
    install_requires=['pytest', 'time', 'datetime', 'enum'],
)   