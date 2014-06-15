# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='tweetable',
    version='1.0',
    maintainer="Max Arnold",
    url="https://github.com/max-arnold/markdown-tweetable",
    py_modules=['tweetable'],
    license='LICENSE.md',
    description='Tweetable quotes for Python-Markdown.',
    keywords = ["markup", "markdown", "plugin", "quotes", "share", "tweet", "social"],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT LIcense",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        ],
    long_description=open('README.md').read(),
)
