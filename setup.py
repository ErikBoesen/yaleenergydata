# Upload package to PyPi.

from setuptools import setup

setup(name='yaleenergydata',
      version='0.1.0',
      description='Library for fetching data from the Yale Energy Data API.',
      url='https://github.com/ErikBoesen/yaleenergydata',
      author='Erik Boesen',
      author_email='me@erikboesen.com',
      license='GPL',
      packages=['yaledining'],
      install_requires=['requests'])
