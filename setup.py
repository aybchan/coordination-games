from setuptools import setup, find_packages

with open('LICENSE') as f:
  license = f.read()

setup(
    name='Coordination-Games',
    version="2.0.0",
    author='Alex Y. Chan',
    author_email='ayb.chan@gmail.com',
    license=license,
    packages=find_packages()
)

