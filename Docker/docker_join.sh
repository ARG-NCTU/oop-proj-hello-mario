#!/usr/bin/env bash

BASH_OPTION=bash

IMG=brian247/aoop2024:hello-mario # Replace with the docker image you pulled

xhost +
containerid=$(docker ps -aqf "ancestor=${IMG}") && echo $containerid
docker exec -it \
    --privileged \
    -e DISPLAY=${DISPLAY} \
    -e LINES="$(tput lines)" \
    ${containerid} \
    $BASH_OPTION
xhost -