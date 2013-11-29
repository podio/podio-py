from setuptools import setup
import sys

try:
   from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
   from distutils.command.build_py import build_py

kw = {}

if sys.version_info >= (3,):
  kw['use_2to3'] = True

setup(
    name="pypodio2",
    version="0.1",
    description="Python wrapper for the Podio API",
    author="Podio",
    author_email="mail@podio.com",
    url="https://github.com/podio/podio-py",
    license="MIT",
    packages=["pypodio2"],
    install_requires=["httplib2"],
    cmdclass = {'build_py': build_py},
    tests_require=["nose", "mock", "tox"],
    test_suite="nose.collector",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    **kw
)
