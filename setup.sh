#!/bin/bash

echo "Construction de l'image docker authentication"
sudo docker build . -f Dockerfile_plantspy -t test_plantspy:latest

echo "Fin de la construction des images docker"

echo "Lancement docker-compose"
sudo docker-compose up


