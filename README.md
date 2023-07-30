# Master Thesis: Diversity in Poetry Generation
This repository contains the code that has been used to conduct experiments in my master thesis about diversity in poetry generation.

## Installation
It is recommended to set up a virtual environment using Conda with Python 3.10. Dependencies will be installed in this environment:
```
conda create -n diversity-in-poetry-generation python=3.10
conda activate diversity-in-poetry-generation
pip install 'git+https://github.com/potamides/uniformers.git#egg=uniformers'
pip install --upgrade gensim
conda install -c conda-forge libarchive
pip install evaluate
pip install matplotlib
pip install cydifflib
pip install lexical-diversity
pip install sentence-transformers
pip install spacy
```

## Data Prepation

Refer to diversity-in-poetry-generation/training_data/ReadMe.md in order to preprocess training data. 

## Generators

#### Deep-speare
#### Structured-Adversary
#### Unconditioned Large Language Models (LLMs)
#### Style-conditioned LLMs

## Analysis
