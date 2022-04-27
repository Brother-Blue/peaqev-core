import setuptools

setuptools.setup(
    name="peaqevcore",
    version="0.0.16",
    author="Magnus Eldén",
    description="Core types for peaqev car charging",
    license="MIT",
    packages=["peaqevcore"],
    install_requires=['pytest', 'datetime', 'statistics'],
)   
