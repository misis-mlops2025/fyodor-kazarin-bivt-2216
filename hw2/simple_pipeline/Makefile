#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = simple_pipeline
PYTHON_VERSION = 3.10
PYTHON_INTERPRETER = python3

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Install Python dependencies
.PHONY: requirements
requirements:
	uv pip install -r requirements.txt
	



## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete


## Lint using ruff (use `make format` to do formatting)
.PHONY: lint
lint:
	ruff format --check
	ruff check

## Format source code with ruff
.PHONY: format
format:
	ruff check --fix
	ruff format

## Validate code with pylint
.PHONY: pylint
pylint:
	$(PYTHON_INTERPRETER) -m pylint simple_pipeline



## Run tests
.PHONY: test
test:
	python3 -m pytest tests

## Run tests with coverage report
.PHONY: coverage
coverage:
	$(PYTHON_INTERPRETER) -m pytest tests --cov=simple_pipeline --cov-report=term-missing --cov-report=html --cov-config=.coveragerc

## Show coverage report
.PHONY: coverage-report
coverage-report:
	$(PYTHON_INTERPRETER) -m coverage report


## Set up Python interpreter environment
.PHONY: create_environment
create_environment:
	uv venv --python $(PYTHON_VERSION)
	@echo ">>> New uv virtual environment created. Activate with:"
	@echo ">>> Windows: .\\\\.venv\\\\Scripts\\\\activate"
	@echo ">>> Unix/macOS: source ./.venv/bin/activate"
	



#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## Generate classification dataset
.PHONY: data
data:
	$(PYTHON_INTERPRETER) -m simple_pipeline.dataset

## Train model
.PHONY: train
train:
	$(PYTHON_INTERPRETER) -m simple_pipeline.modeling.train

## Initialize DVC (if not already done)
.PHONY: dvc-init
dvc-init:
	dvc init --no-scm

## Run DVC pipeline
.PHONY: dvc
dvc:
	dvc repro

## Run specific DVC stage
.PHONY: dvc-stage
dvc-stage:
	dvc repro $(STAGE)

## Show DVC pipeline status
.PHONY: dvc-status
dvc-status:
	dvc status

## Push data to local storage
.PHONY: dvc-push
dvc-push:
	dvc push

## Pull data from local storage
.PHONY: dvc-pull
dvc-pull:
	dvc pull

## Show DVC cache directory size
.PHONY: dvc-cache-size
dvc-cache-size:
	@du -sh .dvc/cache 2>/dev/null || echo "Cache directory not found"

## Clean DVC cache
.PHONY: dvc-cache-clean
dvc-cache-clean:
	dvc cache dir
	dvc cache clean



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
