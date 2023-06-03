FROM debian:11

ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:99
RUN apt-get update && apt-get install -y coreutils dbus-x11 jq lightdm sudo x11vnc xfce4 xorg xvfb

RUN echo 'allowed_users = anybody' >> /etc/X11/Xwrapper.config

COPY setup.sh /
CMD ["/bin/bash", "-c", "chmod +x /setup.sh && /setup.sh"]
#CMD ["service", "ssh", "start"]
