import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="prometheus_express",
    version="0.0.1",
    author="Sean Sube",
    author_email="seansube@gmail.com",
    description="Prometheus client/server for CircuitPython Express ARM devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ssube/prometheus_express",
    keywords=[
        'prometheus',
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)