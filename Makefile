.PHONY: clean data lint requirements 

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROFILE = default
PROJECT_NAME = paris_metro
PYTHON_VERSION = 3.6.2
PYTHON_INTERPRETER = python

requirements: 
	echo 'requirements'

## Download raw data
download:
	src/data/download.sh
	src/data/download_ratp.sh

## Make Dataset
data: requirements
	$(PYTHON_INTERPRETER) src/data/make_dataset.py data/raw/ data/processed/

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
lint:
	flake8 src

## Set up python interpreter environment
create_environment:
	#pyenv install ${PYTHON_VERSION}
	pyenv virtualenv ${PYTHON_VERSION} ${PROJECT_NAME}
	echo ${PROJECT_NAME} > .python-version
