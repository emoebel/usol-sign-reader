# usol-sign-reader

This repository contains an AI-based tool for extracting information from photos of hiking signs.

## Installation

```
$ pip install -r requirements.txt
```

## Usage

First, the trained AI models have to be downloaded. Then, you can run the tool as a bash command:

```
$ signreader -path_models /path/to/AI/models/ -img /path/to/img.jpg -output_folder /path/to/output/folder/
```