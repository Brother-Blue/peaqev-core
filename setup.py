import setuptools

setuptools.setup(
    name="peaqevcore",
    version="0.0.15",
    author="Magnus Eldén",
    description="Core types for peaqev car charging",
    packages=["peaqevcore"],
    install_requires=['pytest', 'datetime', 'statistics'],
)   