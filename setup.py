'''Galoshes
'''

from distutils.core import setup
from setuptools import find_packages

CLASSIFIERS = [
'Development Status :: 3 - Alpha',
'Intended Audience :: Developers',
'Intended Audience :: Science/Research',
'License :: OSI Approved :: MIT License',
'Programming Language :: Python',
'Topic :: Scientific/Engineering',
'Topic :: Scientific/Engineering :: Mathematics',
'Topic :: Scientific/Engineering :: Physics',
'Programming Language :: Python',
'Programming Language :: Python :: 2.7',
'Programming Language :: Python :: 3.3',
'Programming Language :: Python :: 3.4',
'Programming Language :: Python :: 3.5',
'Operating System :: Microsoft :: Windows',
'Operating System :: POSIX',
'Operating System :: Unix',
'Operating System :: MacOS',
'Natural Language :: English',
]

with open('README.md') as fp:
    LONG_DESCRIPTION = ''.join(fp.readlines())

setup(
    name = 'problemo',
    version = '0.2.0',
    packages = find_packages(),
    install_requires = ['numpy>=1.7',
                        'scipy>=0.13',
                        'future',
                       ],
    author = 'Brendan Smithyman',
    author_email = 'brendan@bitsmithy.net',
    description = 'problemo',
    long_description = LONG_DESCRIPTION,
    license = 'MIT',
    keywords = 'sparse linear direct solver',
    url = 'https://github.com/bsmithyman/problemo',
    download_url = 'https://github.com/bsmithyman/problemo',
    classifiers = CLASSIFIERS,
    platforms = ['Windows', 'Linux', 'Solaris', 'Mac OS-X', 'Unix'],
    use_2to3 = False,
)
