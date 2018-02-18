#!/usr/bin/env python
from autodnscli import VERSION
import os.path

from setuptools import find_packages, setup


def readme():
    path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(path):
        with open(path) as f:
            return f.read()


setup(name='autodnscli',
      version=VERSION,
      description='Command line utility for AutoDNS by InternetX',
      long_description=readme(),
      url='https://github.com/osiegmar/autodns-cli',
      author='Oliver Siegmar',
      author_email='oliver@siegmar.de',
      license='Apache License (2.0)',
      keywords="autodns internetx cli",
      zip_safe=True,
      packages=find_packages(),
      install_requires=['argparse', 'requests'],
      entry_points={'console_scripts': [
          'autodns=autodnscli.autodns:main'
          ]
      },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Natural Language :: English',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Internet :: Name Service (DNS)',
          'Topic :: Utilities'
      ]
      )
