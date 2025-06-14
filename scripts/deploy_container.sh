# deploy_container.sh
#!/bin/bash

# Set image name and container name
IMAGE_NAME="hft_trading_simulator"
CONTAINER_NAME="hft_simulator_container"

echo "Building the Docker image..."
docker build -t ${IMAGE_NAME} .

echo "Stopping any existing container with the same name..."
docker rm -f ${CONTAINER_NAME} 2>/dev/null

echo "Running the container..."
docker run -d --name ${CONTAINER_NAME} -p 5000:5000 ${IMAGE_NAME}

echo "Container ${CONTAINER_NAME} is now running."
