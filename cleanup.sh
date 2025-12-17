#!/bin/bash

CLUSTER_NAME="jobbot"

echo "Cleaning up JobBot environment..."

if kind get clusters | grep -q "^$CLUSTER_NAME$"; then
    echo "Deleting cluster: $CLUSTER_NAME..."
    kind delete cluster --name $CLUSTER_NAME
else
    echo "Cluster $CLUSTER_NAME does not exist."
fi

echo "Removing local build images..."
docker rmi jobbot-bot:latest jobbot-scraper:latest 2>/dev/null

echo "Cleanup finished."