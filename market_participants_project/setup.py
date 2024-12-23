from setuptools import setup, find_packages

setup(
    name="market_participants",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'pyarrow' 
    ],
)