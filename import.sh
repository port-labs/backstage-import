#!/bin/bash

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker to proceed."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "The .env file is missing. Please make sure to create the .env file and set the required environment variables. (PORT_CLIENT_ID, PORT_CLIENT_SECRET, BACKSTAGE_URL))"
    exit 1
fi

# Check if .env file contains required keys
required_keys=("PORT_CLIENT_ID" "PORT_CLIENT_SECRET" "BACKSTAGE_URL")
missing_keys=()

for key in "${required_keys[@]}"; do
    if ! grep -q "^$key=" .env; then
        missing_keys+=("$key")
    fi
done

if [ ${#missing_keys[@]} -gt 0 ]; then
    echo "The .env file is missing the following required keys: ${missing_keys[*]}. Please make sure all required keys are set."
    exit 1
fi

# Build and run the Docker container
docker build -t backstage-import . && docker run --env-file=.env backstage-import
