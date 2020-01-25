from setuptools import setup


# Get the long description from the README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(name="json_configparser",
      version="0.4.2",
      description="A module that parses and validates JSON configuration files.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/GIlunga/JSON-Configparser",
      author="Guilherme Ilunga",
      author_email="guiilunga@hotmail.com",
      classifiers=["Development Status :: 3 - Alpha",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Programming Language :: Python :: 3.6",
                   "Programming Language :: Python :: 3.7",
                   "Programming Language :: Python :: 3.8"],
      keywords="configuration options",
      packages=["json_configparser"],
      python_requires=">=3.6, <3.9",
      install_requires=[],
      project_urls={"Bug Reports": "https://github.com/GIlunga/JSON-Configparser/issues",
                    "Source": "https://github.com/GIlunga/JSON-Configparser"})
