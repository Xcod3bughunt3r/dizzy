#!/usr/bin/env python3

from setuptools import setup
from dizzy.config import CONFIG

setup(name='dizzy',
      version=CONFIG["GLOBALS"]["VERSION"],
      description='Dizzy Fuzzing Library',
      author='Daniel Mende',
      author_email='mail@c0decafe.de',
      url='https://c0decafe.de',
      license='MIT',
      classifiers=[ 'Development Status :: 4 - Beta',
                    'Environment :: Console',
                    'License :: OSI Approved :: MIT License',
                    'Natural Language :: English ',
                    'Operating System :: POSIX',
                    'Operating System :: Microsoft :: Windows',
                    'Programming Language :: Python :: 3 :: Only',
                    'Topic :: Security',
                    'Topic :: Software Development :: Testing'],
      packages=['dizzy', 'dizzy.encodings', 'dizzy.functions', 'dizzy.objects', 'dizzy.probe', 'dizzy.session'],
      scripts=['dizzy_cmd'],
      data_files=[('./share/dizzy/', ['./lib/std_string_lib.txt'])],
      python_requires='>=3',
      install_requires=[
          'exrex',
          'pcapy',
      #    'Crypto'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      )
