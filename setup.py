import setuptools

setuptools.setup(
    name="peaqevcore",
    version="2.0.2",
    author="Magnus Eldén",
    description="Core types for peaqev car charging",
    url="https://github.com/elden1337/peaqev-core",
    license="MIT",
    packages=[
        "peaqevcore", 
        "peaqevcore.locale_service", 
        "peaqevcore.country_service",
        "peaqevcore.hourselection_service", 
        "peaqevcore.hourselection_service.models", 
        "peaqevcore.chargecontroller_service", 
        "peaqevcore.models", 
        "peaqevcore.prediction_service", 
        "peaqevcore.session_service",
        "peaqevcore.threshold_service", 
        "peaqevcore.locale_service.querytypes", 
        "peaqevcore.locale_service.querytypes.models"
        ],
    test_requires=['pytest']
)   
