from setuptools import setup

with open("./requirements.txt", "r") as f:
    required = f.read().splitlines()

setup(
  name='Lorrelate',
  version='0.1.0',
  author='Jacob Kienast',
  author_email='jcb.seifert@gmail.com',
  packages=['lorrelate'],
  scripts=['bin/lot',],
  url='https://github.com/jcbs/lorrelate',
  license='LICENSE.txt',
  description='Correlates log events by time',
  long_description=open('README.md').read(),
  install_requires=required,
)
