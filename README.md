# usol-sign-reader

This repository contains an AI-based tool for extracting information from photos of hiking signs.

## Installation
Create and activate a virtual environment with conda:
```
$ conda create -n signreader python=3.10
$ conda activate signreader
```
Install code from github repository:
```
$ pip install git+https://github.com/emoebel/usol-sign-reader.git
```
Test if installation is successful:
```
$ cd /path/to/usol-sign-reader/tests
$ python test_text_reader.py
$ python test_sign_detector.py
$ python test_symbol_detector.py
```

## Usage

First, the trained AI models have to be downloaded. Then, you can run the tool as a bash command:

```
$ signreader -models /path/to/AI/models/ -image /path/to/img.jpg -out /path/to/output/folder/
```

The path to the models folder is expected to be structured as follows:
```
models
|-cellpose
|  |-model_file
|-yolo
|  |-model_file.pt
```

## Repository content
- signreader: source code
- examples: python scripts with usage examples
- tests: unit tests
- scripts: python scripts I used for constituting the datasets. May be a bit messy.
- notebooks: jupyter notebooks I used for prototyping the pipeline. Also contains the Colab notebooks for training the AI models.