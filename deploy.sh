#!/bin/bash

CLUSTER_NAME="jobbot"
BOT_IMAGE="jobbot-bot:latest"
SCRAPER_IMAGE="jobbot-scraper:latest"

echo "Starting JobBot Deployment..."

echo "Building Discord Bot..."
docker build -t $BOT_IMAGE -f bot/Dockerfile.bot ./bot

echo "Building Scraper..."
docker build -t $SCRAPER_IMAGE -f scrapers/Dockerfile.scraper ./scrapers

if ! kind get clusters | grep -q "^$CLUSTER_NAME$"; then
    echo "Creating cluster..."
    kind create cluster --name $CLUSTER_NAME
fi

echo "Loading images into Kind..."
kind load docker-image $BOT_IMAGE --name $CLUSTER_NAME
kind load docker-image $SCRAPER_IMAGE --name $CLUSTER_NAME

echo "Applying manifests..."

if [ -f "bot/discord-bot-pod.yaml" ]; then
    kubectl apply -f bot/discord-bot-pod.yaml
else
    echo "Error: bot/discord-bot-pod.yaml not found!"
fi

if [ -f "scrapers/github-scraper.yaml" ]; then
    kubectl apply -f scrapers/github-scraper.yaml
else
    echo "Error: scrapers/github-scraper.yaml not found!"
fi

echo "Done! Current Pods:"
kubectl get pods