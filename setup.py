import setuptools

setuptools.setup(
    name="peaqevcore",
    version="1.0.19",
    author="Magnus Eldén",
    description="Core types for peaqev car charging",
    url="https://github.com/elden1337/peaqev-core",
    license="MIT",
    packages=[
        "peaqevcore", 
        "peaqevcore.locale", 
        "peaqevcore.country", 
        "peaqevcore.locale.querytypes", 
        "peaqevcore.locale.querytypes.models"
        ],
    test_requires=['pytest']
)   
