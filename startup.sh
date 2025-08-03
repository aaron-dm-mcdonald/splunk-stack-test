#!/bin/bash



dnf install -y docker git
curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
systemctl enable --now docker

mkdir splunk && cd splunk
git clone https://github.com/aaron-dm-mcdonald/splunk-stack-test.git .

# get images first
docker-compose pull

# Start the stack
docker-compose up -d

sleep 60

docker-compose logs > stack.logs


