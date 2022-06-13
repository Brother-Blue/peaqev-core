import setuptools

setuptools.setup(
    name="peaqevcore",
    version="1.0.13",
    author="Magnus Eldén",
    description="Core types for peaqev car charging",
    url="https://github.com/elden1337/peaqev-core",
    license="MIT",
    packages=["peaqevcore", "peaqevcore.locale", "peaqevcore.country"],
    test_requires=['pytest']
)   
