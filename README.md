# usol-sign-reader

This repository contains an AI-based tool for extracting information from photos of hiking signs.

## Installation

```
$ pip install git+https://github.com/emoebel/usol-sign-reader.git
```

## Usage

First, the trained AI models have to be downloaded. Then, you can run the tool as a bash command:

```
$ signreader -path_models /path/to/AI/models/ -img /path/to/img.jpg -output_folder /path/to/output/folder/
```

The path to the models folder is expected to be structured as follows:
```
models
|-cellpose
   |-model_file
|-yolo
   |-model_file.pt
```

## Repository content
- signreader: source code
- examples: python scripts with usage examples
- tests: unit tests (will not work for now because input data is not contained in this repo)
- scripts: python scripts I used for constituting the datasets. May be a bit messy.
- notebooks: jupyter notebooks I used for prototyping the pipeline. Also contains the Colab notebooks for training the AI models.