#!/usr/bin/env bash

PARENT_DIR=${PWD%/*}
IMAGE_NAME=${PARENT_DIR##*/}
CONTAINER_NAME="${IMAGE_NAME}_container"
XAUTH=/tmp/.docker.xauth

echo "Building docker image: ${IMAGE_NAME}"
docker build -t ${IMAGE_NAME} . > /dev/null 2>&1

if [ ! -f $XAUTH ]; then
    xauth_list=$(xauth nlist $DISPLAY)
    xauth_list=$(sed -e 's/^..../ffff/' <<<"$xauth_list")
    if [ ! -z "$xauth_list" ]; then
        echo "$xauth_list" | xauth -f $XAUTH nmerge -
    else
        touch $XAUTH
    fi
    chmod a+r $XAUTH
fi

if [ ! -f $XAUTH ]; then
    echo "[$XAUTH] was not properly created. Exiting..."
    exit 1
fi

if [ $? -ne 0 ]; then
    echo "Docker image built failed"
    exit 1
fi

xhost +
docker run \
    -it \
    --rm \
    --name ${CONTAINER_NAME} \
    -e DISPLAY=$DISPLAY \
    -v "/tmp/.X11-unix:/tmp/.X11-unix" \
    -v "/home/$USER/$IMAGE_NAME:/home/arg/$IMAGE_NAME" \
    --device /dev/snd:/dev/snd \
    --privileged \
    --net=host \
    ${IMAGE_NAME}
xhost -