set -x
set -e
PREFIX="diomwu"
IMAGE_NAME="hashcache-global-proxy"
TAG="latest"
DOCKER_IMAGE="$PREFIX/$IMAGE_NAME:$TAG"
echo "Building $DOCKER_IMAGE ..."
docker build -t $DOCKER_IMAGE .
docker push $DOCKER_IMAGE