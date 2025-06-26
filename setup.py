import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="signreader",
    version="0.0.1",
    author="Emmanuel Moebel",
    author_email="emmanuel.moebel@gmail.com",
    description=("AI-based tool for extracting information from photos of hiking signs."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience:: Developers",
        "Programming Language:: Python",
        "Programming Language:: Python:: 3",
        "Programming Language:: Python:: 3.10",
        "Operating System:: OS Independent",
    ],
    install_requires=[
        "cellpose==4.0.4",
        "ultralytics==8.3.156",
        "moondream==0.1.0",
        "numpy==2.1.3",
        "scikit-image==0.25.2",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "signreader = signreader.__main__:main",
        ]
    }
)