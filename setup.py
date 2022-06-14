import setuptools

setuptools.setup(
    name="peaqevcore",
    version="1.0.14",
    author="Magnus Eldén",
    description="Core types for peaqev car charging",
    url="https://github.com/elden1337/peaqev-core",
    license="MIT",
    packages=["peaqevcore", "peaqevcore.locale", "peaqevcore.country", "peaqevcore.locale.querytypes"],
    test_requires=['pytest']
)   
