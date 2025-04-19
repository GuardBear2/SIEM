#!/bin/bash
# Script to pull Docker image from GitHub Container Registry

GITHUB_TOKEN=$1
GITHUB_USER=$2
CONTAINER_NAME=$3
DOCKER_IMAGE_TAG=$4
GITHUB_OWNER="nikinov"

echo "Logging in to GitHub Container Registry"
echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USER --password-stdin

echo "Pulling Docker image from GitHub Container Registry: ghcr.io/${GITHUB_OWNER}/${CONTAINER_NAME}:${DOCKER_IMAGE_TAG}"
docker pull ghcr.io/${GITHUB_OWNER}/${CONTAINER_NAME}:${DOCKER_IMAGE_TAG}

if [ $? -ne 0 ]; then
  echo "Error: Failed to pull Docker image ghcr.io/${GITHUB_OWNER}/${CONTAINER_NAME}:${DOCKER_IMAGE_TAG}"
  exit 1
fi

# Tag the image with the expected name
echo "Tagging image as ${CONTAINER_NAME}:${DOCKER_IMAGE_TAG}"
docker image tag ghcr.io/${GITHUB_OWNER}/${CONTAINER_NAME}:${DOCKER_IMAGE_TAG} ${CONTAINER_NAME}:${DOCKER_IMAGE_TAG} 