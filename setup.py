from setuptools import setup
from glob import glob

data = glob('freetshirts/*.csv')

setup(name='freetshirts',
      version='0.1',
      description='Package to generate email with personalized message to 1500+ colleges.',
      url='http://github.com/iiradia/freetshirts',
      author='Ishaan Radia',
      author_email='iiradia@ncsu.edu',
      license='MIT',
      packages=['freetshirts'],
      install_requires = ['pandas'],
      package_data = {"freetshirts": 
            data
      },
      zip_safe=False)