FROM argnctu/oop:latest

ENV DISPLAY=:0
ENV QT_X11_NO_MITSHM=1
ENV XAUTHORITY=/tmp/.docker.xauth

WORKDIR /home/arg/oop-proj-hello-mario

COPY . .

USER root

RUN chmod +x require.sh && ./require.sh
RUN chmod 777 /tmp/.X11-unix
CMD ["bash"]
