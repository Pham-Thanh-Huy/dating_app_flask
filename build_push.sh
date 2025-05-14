version=$1
docker build -t datting-app:${version:-latest} .
