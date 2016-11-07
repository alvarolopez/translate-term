# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup


version = re.search(
    "^__version__\s*=\s*'(.*)'",
    open('translate/translate.py').read(),
    re.M
    ).group(1)

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name = 'translate-term',
    packages = ['translate'],
    install_requires=[
        'requests>=2.8.1',
        'beautifulsoup4>=4.4.1',
        'terminaltables>=2.1.0'
        ],
    entry_points = {
        'console_scripts': ['translate = translate.translate:main']
        },
    version = version,
    description = 'Command line translator pulling from wordreference.com and coded in Python',
    long_description = long_descr,
    keywords='shell bash zsh terminal translate wordreference',
    license='MIT',
    author = 'Kevin Olivier',
    author_email = 'kevin.olivier@outlook.com',
    url = 'https://github.com/kevinolivier/translate-term'
    )

