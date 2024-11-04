FROM argnctu/oop:latest

ARG DISPLAY
ENV DISPLAY=${DISPLAY}
ENV QT_X11_NO_MITSHM=1
ENV XAUTHORITY=/tmp/.docker.xauth

WORKDIR /home/arg/oop-proj-hello-mario

COPY . .

USER root

RUN ls -la /home/arg/oop-proj-hello-mario

RUN chmod +x /home/arg/oop-proj-hello-mario/require.sh && .home/arg/oop-proj-hello-mario/require.sh

CMD ["bash"]
