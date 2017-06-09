from setuptools import setup, find_packages
import os

dev_requirements = [
    'prospector',
    'tox',
    'twine',
]

setup(
    name='changelog-cli',
    description='Command line interface for managing CHANGELOG.md files',
    version=os.getenv('MODULE_VERSION_ID', '0.1.0'),
    author='Ryan McDevitt',
    author_email='mcdevitt.ryan@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'click'
    ],
    extras_require={'dev': dev_requirements},
    entry_points={
        'console_scripts': [
            'changelog=runner:cli',
            'cl=runner:cli'
        ]
    }
)
