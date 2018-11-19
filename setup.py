from distutils.core import setup

setup(
    name='prevedere',
    version='0.1',
    packages=['prevedere',],
    install_requires=[
        'requests',
        'pandas',
    ],
    url="https://github.com/prevedere/prevedere_api",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
)