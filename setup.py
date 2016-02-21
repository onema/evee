# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__version__ = '0.1.0'

setup(
        name='evee',
        license='MIT',
        version=__version__,
        description='Evee is an event dispatcher port of the Symfony Event Dispatcher Component. It allows your '
                    'applications to communicate with one another by dispatching and listening for events.',
        long_description=open('README.md').read(),
        author='Juan Manuel Torres',
        author_email='kinojman@gmail.com',
        url='https://github.com/onema/evee',
        download_url='https://github.com/onema/evee/archive/v%s.tar.gz' % __version__,
        packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
        zip_safe=True,
        test_suite='nose.collector',
        tests_require=['nose', 'coverage'],
        classifiers=[
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
)