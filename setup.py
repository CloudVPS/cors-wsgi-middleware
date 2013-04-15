#!/usr/bin/python
#-*- coding:utf-8 -*-

from setuptools import setup

setup(
    name='corswsgi',
    version="1.0.0",
    description="Cors wsgi filter",
    py_modules=["corswsgi"],
    entry_points = {
        'paste.filter_factory': [
            'corswsgi=corswsgi:filter_factory',
        ]
    }
)