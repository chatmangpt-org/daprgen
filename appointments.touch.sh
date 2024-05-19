#!/bin/bash

# Base directories
SRC_DIR="./src/daprgen"
TESTS_DIR="./tests"

# Appointments directories
APPOINTMENTS_SRC_DIR="${SRC_DIR}/appointments"
APPOINTMENTS_TESTS_DIR="${TESTS_DIR}/appointments"

# Create directories
mkdir -p "${APPOINTMENTS_SRC_DIR}"
mkdir -p "${APPOINTMENTS_TESTS_DIR}"

# Create __init__.py files
touch "${APPOINTMENTS_SRC_DIR}/__init__.py"
touch "${APPOINTMENTS_TESTS_DIR}/__init__.py"

# Create other necessary files
touch "${APPOINTMENTS_SRC_DIR}/models.py"
touch "${APPOINTMENTS_SRC_DIR}/repository.py"
touch "${APPOINTMENTS_SRC_DIR}/service.py"
touch "${APPOINTMENTS_SRC_DIR}/factory.py"
touch "${APPOINTMENTS_SRC_DIR}/api.py"

touch "${APPOINTMENTS_TESTS_DIR}/test_models.py"
touch "${APPOINTMENTS_TESTS_DIR}/test_repository.py"
touch "${APPOINTMENTS_TESTS_DIR}/test_service.py"
touch "${APPOINTMENTS_TESTS_DIR}/test_factory.py"
touch "${APPOINTMENTS_TESTS_DIR}/test_api.py"

echo "Created appointments directories and files in src and tests directories."
