import setuptools

setuptools.setup(
    name="peaqevcore",
    version="1.1.1",
    author="Magnus Eldén",
    description="Core types for peaqev car charging",
    url="https://github.com/elden1337/peaqev-core",
    license="MIT",
    packages=[
        "peaqevcore", 
        "peaqevcore.locale", 
        "peaqevcore.country",
        "peaqevcore.hourselection", 
        "peaqevcore.locale.querytypes", 
        "peaqevcore.locale.querytypes.models"
        ],
    test_requires=['pytest']
)   
