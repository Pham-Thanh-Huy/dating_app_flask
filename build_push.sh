#!/bin/sh

tag=$1
IMAGE_NAME=datting-app

echo "----> Building image"
if docker build -t ${IMAGE_NAME}:${tag:-latest} -f Dockerfile .; then
  echo "----> Done"
else
  echo "----> Error to build image!"
  exit 1
fi


