from setuptools import setup, find_packages
from os.path import join, dirname

setup (name = 'ugit',
        version = '1.0',
        packages = ['ugit'],
        entry_points = {
            'console_scripts': [
                'ugit = ugit.cli:main'
                ]
            },
        )
