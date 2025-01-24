# Copyright (C) 2022 CBRE, Inc. All rights reserved.

# The container registry type
# i.e., aws, gcloud or artifactory-base
REGISTRY = artifactory-nonprod
 
# The kubernetes namespace where the deployment and service
# resources will be placed, this value also affects the service fqdn
NAMESPACE = app-finance-fte

# The kubernetes label/taint placed on a node where the 
# deployment and service resources will be placed.
NODE_LABEL_NAME = xero-lambda
 
## The input type name (by convention only, not an actual type)
# e.g., photo, text, etc.
DATATYPE = event

# The inference being performed (again, by convention only)
# e.g., entity, blocking, regression, etc.
OPERATION = fte-calculator

# The container image name, used for the registry and deployment
IMAGE = $(NAMESPACE)-$(DATATYPE)-$(OPERATION)

# The container image version, typically we use the git tag,
# e.g., git tag v1.0.0; git push origin develop --tags
VERSION ?= $(shell git fte --abbrev=0 --tags)

REPLICAS ?= 1

DOCKER_FILE = Dockerfile

MODEL_FILE ?= FTE_Calc_wc.pkl

DOCKER_BUILD_EXTRA_FLAGS = --build-arg MODEL_FILE_BT='${MODEL_FILE}'  

# build default
default: docker_build

include ../edp-xero-core/base.make
