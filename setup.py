from setuptools import setup, find_packages

with open('LICENSE') as f:
  license = f.read()

setup(
    name='hypergraph-games',
    version="2.1.0",
    author='Alex Y. Chan',
    author_email='ayb.chan@gmail.com',
    license=license,
    packages=find_packages()
)

