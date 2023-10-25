from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

VERSION = '0.0.1'
DESCRIPTION = 'A straightforward wrapper for the IsItDownRightNow API.'
LONG_DESCRIPTION = "An accessible worldwide website availability checker library, enabling real-time checks for a specific website's global accessibility."

# Setting up
setup(
    name='isitdownrightnow',
    version=VERSION,
    author='ccan23',
    author_email='dev.ccanb@protonmail.com',
    url='https://github.com/ccan23/isitdownrightnow',
    license='MIT',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=install_requires,
    keywords=['python', 'uptime', 'server', 'website', 'down', 'ping'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License'
    ]
)