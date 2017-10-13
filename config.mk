# default config values that can all be overridden
VE ?= ./ve
MANAGE ?= ./manage.py
FLAKE8 ?= $(VE)/bin/flake8
SYS_PYTHON ?= python3
PIP ?= $(VE)/bin/pip3
SENTINAL ?= $(VE)/sentinal
PYPI_URL ?= https://pypi.ccnmtl.columbia.edu/
WHEEL_VERSION ?= 0.30.0
REQUIREMENTS ?= requirements.txt
VIRTUALENV ?= virtualenv.py
SUPPORT_DIR ?= requirements/virtualenv_support/
WHEELHOUSE ?= wheelhouse

JS_FILES ?= media/js/
TAG ?= latest
IMAGE ?= $(REPO)/$(APP):$(TAG)

MAX_COMPLEXITY ?= 10

