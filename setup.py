from setuptools import setup, find_packages
import os

VERSION_FILE = 'src/changelog/_version.py'
with open(VERSION_FILE, 'r') as vf:
    value = vf.read()
v = value.split('=')[1].strip().strip('"')

dev_requirements = [
    'coverage',
    'invoke',
    'mock',
    'prospector',
    'twine',
    'wheel'
]

setup(
    name='changelog-cli',
    description='Command line interface for managing CHANGELOG.md files',
    long_description=open("README.md", 'r').read(),
    long_description_content_type='text/markdown',
    version=os.getenv('MODULE_VERSION_ID', v),
    author='Ryan McDevitt',
    author_email='mcdevitt.ryan@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/mc706/changelog-cli',
    license="MIT",
    install_requires=[
        'click'
    ],
    extras_require={'dev': dev_requirements},
    entry_points={
        'console_scripts': [
            'changelog=changelog.commands:cli',
            'cl=changelog.commands:cli'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Documentation',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Documentation',
        'Topic :: Utilities',
    ]
)
