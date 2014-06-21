# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='markdown-tweetable',
    version='1.1.0',
    maintainer="Max Arnold",
    maintainer_email="arnold.maxim@gmail.com",
    url="https://github.com/max-arnold/markdown-tweetable",
    packages=['tweetable'],
    install_requires=['Markdown >= 2.0'],
    license='LICENSE.md',
    description='Tweetable quotes for Python-Markdown.',
    keywords=["markup", "markdown", "plugin", "quotes", "share", "tweet", "social"],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        ],
    long_description=open('README.md').read(),
)
