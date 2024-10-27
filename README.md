# Game Demo
![Game Demo GIF](docs/mario.gif)

# Class Diagram of main program
![Class Diagram](docs/classes.png)

# Tasks before running the game
## Team Leader
1. Create a **Docker Hub account**.
2. Log in your docker hub and create a new repository to store the built images. Make sure to set it to `Public`
3. Enter the directory `~/oop-proj-hello-mario/Docker`
4. Enter your own docker hub account and repository in `build.sh`, `docker_run.sh` and `docker_join.sh`
5. Let your team members know where the built image will be.

## Team Member
1. Create a **Docker Hub account**.
2. Log in your docker hub.
3. Enter the directory `~/oop-proj-hello-mario/Docker`
3. Enter your team leader's docker hub account, repository and tag name **ONLY** in the `docker_run.sh` and `docker_join.sh`

# Use Docker As Root
First open the terminal and type
```
$ sudo groupadd -f docker
```
Then type the following usermod command to add the active user to the **docker** group
```
$ sudo usermod -aG docker $USER
```
Apply the group changes to the current terminal session by typing
```
$ newgrp docker
```
Finally check if the **docker** group is in the list of user groups
```
$ groups
```

# How to run the game
First enter the repo
```
$ cd oop-proj-hello-mario
```
Build the docker image first (team leader only)
```
./docker_build
```
The process requires docker hub account. There will be messages about loggin in to docker hub account before you build the image.

After the images is built and pushed to docker hub, both team leader and member can run
```
$ ./docker_run
```
If the docker container is in process, please run
```
$ ./docker_join
```
Run this command to enter the game after the container is running
```
# python3 main.py
```
# Audio Device issue handling
This game requires your audio device. The default is set to `hw:0,0` beforehand.

If there are any error messages related to `ALSA`, please run the following command:
```
# aplay -l
```
This command shows all your available audio devices.

If you have an available audio device, run the following:
```
# export AUDIODEV=hw:(#card_number),(#device_number)
```
Choose the audio device you want to use from the above list.

e.g.

![aplay example image](docs/aplay_example.png)

`HDA Analog` is the name of the laptop, and it's on `card 0`, `device 0`. So we enter
```
# export AUDIODEV=hw:0,0
```
Test if successful by running the following command
```
# speaker-test -D hw:(#card_number),(#device_number) -t wav -c 2
```
If you hear sounds playing, congratulations! You're ready to run the game.
