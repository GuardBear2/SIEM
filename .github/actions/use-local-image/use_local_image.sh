#!/bin/bash
# Script to pull Docker image from Docker Hub

CONTAINER_NAME=$1
DOCKER_IMAGE_TAG=$2
DOCKER_HUB_USER="nikinov"

echo "Pulling Docker image from Docker Hub: ${DOCKER_HUB_USER}/${CONTAINER_NAME}:${DOCKER_IMAGE_TAG}"
docker pull ${DOCKER_HUB_USER}/${CONTAINER_NAME}:${DOCKER_IMAGE_TAG}

if [ $? -ne 0 ]; then
  echo "Error: Failed to pull Docker image ${DOCKER_HUB_USER}/${CONTAINER_NAME}:${DOCKER_IMAGE_TAG}"
  exit 1
fi

# Tag the image with the expected name
echo "Tagging image as ${CONTAINER_NAME}:${DOCKER_IMAGE_TAG}"
docker tag ${DOCKER_HUB_USER}/${CONTAINER_NAME}:${DOCKER_IMAGE_TAG} ${CONTAINER_NAME}:${DOCKER_IMAGE_TAG} 