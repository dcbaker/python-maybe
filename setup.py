from setuptools import setup, find_packages
from codecs import open
from os import path

import maybe

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='python-maybe',
    version=maybe.__version__,
    description='A maybe pattern implementaiton for python',
    long_description=long_description,
    url='https://github.com/dcbaker/python-maybe',
    author='Dylan Baker',
    author_email='dylan@pnwbakers.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Developers',
    ],
    extras_require={
        'test': [
            'pytest',
        ]
    },
    keywords='maybe',
    packages=['maybe'],
)
