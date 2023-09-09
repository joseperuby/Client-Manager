from setuptools import setup, find_packages

setup(
    name='Client-Manager-joseperuby',
    version='1.0',
    description='Client Manager with GUI for csv files',
    long_description=open('README.md').read(),
    author='Jose Luis Ramirez Larios',
    author_email='peperala34@gmail.com',
    url='https://github.com/joseperuby',
    license_files=['LICENSE'],
    packages= find_packages(),
    test_suite='tests',
    scripts=['run.py']
)