#!/usr/bin/python3

from contextlib import closing
from json import dumps
from os.path import join
from python_on_whales import docker
from random import choice
from rich.console import Console
from subprocess import Popen, PIPE
from tempfile import TemporaryDirectory
from time import sleep
import socket
import string

console = Console()
plist = string.ascii_letters + string.digits

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def generate():
    config = {
            'username': ''.join(choice(string.ascii_letters) for k in range(8)),
            'password': ''.join(choice(plist) for k in range(16)),
            'vncpasswd': ''.join(choice(plist) for k in range(8))
            }
    
    return config

def spawn():
    config = generate()
    with TemporaryDirectory() as tempdir:
        with open(join(tempdir, 'config.json'), 'w+') as file:
            file.write(dumps(config))
        
        port = find_free_port()
        container = docker.create('deb-vnc', volumes = [(tempdir, '/mnt', 'ro')], publish=[(port, 5900)])
        out = container.start(attach=True, stream=True)

        console.print(f'Port: {port}\nVNC Password: {config["vncpasswd"]}\nUsername: {config["username"]}\nPassword: {config["password"]}')
        try:
            for stype, scontent in out:
                if 'PORT=5900' in scontent.decode():
                    break

        except KeyboardInterrupt:
            container.kill()

        console.print('[light green]Container started![/light green]')
        sleep(1)
        vnc_process = Popen(['/bin/bash', '-c', f"VNC_PASSWORD={config['vncpasswd']} vncviewer 127.0.0.1:{port}"], stdout=PIPE, stderr=PIPE)
        
        while vnc_process.poll() == None:
            pass

        container.kill()



spawn()        
        

