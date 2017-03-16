#!/usr/bin/env python

import sys, os
from setuptools import setup
from setuptools.command.test import test as TestCommand

exec(open(os.path.join(
    os.path.dirname(__file__), 'modron/version.py'
)).read())


if sys.version_info < (3, 5):
    raise RuntimeError('%s requires python 3.5+' % __package_name__)

class PytestCommand(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['modron']
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))

class PylintCommand(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pylint.lint
        pylint.lint.Run(['--reports=n', 'modron'])

class PyCodeStyleCommand(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pycodestyle
        style_guide = pycodestyle.StyleGuide()
        report = style_guide.check_files(['modron'])
        if report.total_errors:
            sys.exit(1)
        else:
            sys.exit(0)

install_requires = [
    'pandas>=0.19.0',
    'requests>=2.13.0'
]

test_requires = [
    'pytest==3.0.7',
    'pylint==1.6.5',
    'pycodestyle==2.3.1',
    'httpretty==0.8.14'
]

entry_points = {
    'console_scripts': [
        'modron=modron.__main__:main'
    ]
}

cmdclass = {
    'test': PytestCommand,
    'lint': PylintCommand,
    'style': PyCodeStyleCommand
}

setup(
    name=__package_name__,
    version=__version__,
    description='A well-behaved data cleaning ingestion library',
    author='Morgan Jones',
    author_email='mjones@rice.edu',
    license='MIT',
    packages=['modron'],
    install_requires=install_requires,
    tests_require=test_requires,
    entry_points=entry_points,
    cmdclass=cmdclass
)
