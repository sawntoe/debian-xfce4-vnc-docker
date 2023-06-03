# Debian XFCE4 VNC Docker

A simple XFCE4 debian VNC docker.

Only prod.Dockerfile and setup.sh are required for building the docker, but config.json is required during runtime. An example config has been provided.

## Building

Run `make` to build the docker.

## Running

A readonly volume at `/mnt`, containing a config.json is required at startup.

To run, use the following command:
```
# docker run --rm -it -v <directory-containing-config.json>:/mnt -p <port-for-vnc-server>:5900 deb-vnc
```
## Using launch.py

`launch.py` requires tigervnc, and the python modules `rich` and `python_on_whales` to be installed on the host machine. Build the container using `make`, and run `launch.py` to get a seamless vm-like experience.
