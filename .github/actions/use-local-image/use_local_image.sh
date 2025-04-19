#!/bin/bash
# Script to use local Docker image instead of pulling from GHCR

CONTAINER_NAME=$1
DOCKER_IMAGE_TAG=$2

# Check if the image exists locally
if docker image inspect ${CONTAINER_NAME}:${DOCKER_IMAGE_TAG} > /dev/null 2>&1; then
  echo "Using local Docker image ${CONTAINER_NAME}:${DOCKER_IMAGE_TAG}"
else
  echo "Error: Local Docker image ${CONTAINER_NAME}:${DOCKER_IMAGE_TAG} not found"
  exit 1
fi

# No need to tag as it's already correctly named 