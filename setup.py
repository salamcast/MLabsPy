import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AbuKhadeejah", # Replace with your own username
    version="0.0.1",
    author="Abu Khadeejah Karl",
    author_email="salamcast@gmail.com",
    description="Motion Labs PM-XXX log file parser and plot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/salamcast/MLabsPy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
