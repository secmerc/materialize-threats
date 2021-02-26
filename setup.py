import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="materialize-threats-nathan",
    version="1.0.0",
    author="Nathan Sfard",
    author_email="author@example.com",
    description="Copy of secmerc's materialize threats to test pypi publishing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sfc-gh-nsfard/materialize-threats",
    packages=setuptools.find_packages(),
    install_requires=[
          'peewee',
          'gherkin-official',
          'pytest'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points = {
        'console_scripts': ['materialize-threats=materialize_threats.materialize:ThreatMaterializer.materialize'],
    }
)
