from setuptools import setup

extras = {
    'test': [
        'mock',
        'nose',
        'tox',
    ]
}

setup(
    name="pypodio2",
    version="1.0.0b0",
    description="Python wrapper for the Podio API",
    author="Podio",
    author_email="mail@podio.com",
    url="https://github.com/podio/podio-py",
    license="MIT",
    packages=["pypodio2"],
    install_requires=[
        "httplib2",
        "future",
    ],
    extras_require=extras,
    test_suite="nose.collector",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
