#!/bin/bash

mkdir splunk && cd splunk

# non-prod install script
curl -fsSL https://get.docker.com -o get-docker.sh
chmod +x get-docker.sh
./get-docker.sh

git clone https://github.com/aaron-dm-mcdonald/splunk-stack-test.git .

# get images first
docker-compose pull

# Start the stack
docker-compose up -d

sleep 60

docker-compose logs > stack.logs


