import setuptools

with open("README.md", "r") as fh:
        long_description = fh.read()

setuptools.setup(
    name='prevedere-api',
    version='0.1',
    author="Prevedere, Inc.",
    author_email="support@prevedere.com",
    description="API interface for Prevedere Inc. in Python 3.6+",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url="https://github.com/prevedere/prevedere_api",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: Free To Use But Restricted",
        "Operating System :: OS Independent",
    ],
)
