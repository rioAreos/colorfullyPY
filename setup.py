from setuptools import setup, find_packages

setup(
    name="colorfullyPY",
    version="0.0.1",
    packages=find_packages(),
    author="Uoc & Rio",
    description="Colors your colorless Terminal!",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RioAreos/colorfullyPY",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
