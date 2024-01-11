#!/usr/bin/python3
"""Module for web app deployment"""
from fabric.api import put, run, env
from os.path import exists

env.hosts = ['18.204.14.56', '35.153.226.169']


def do_deploy(archive_path):
    """deploy the web_static files to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file = archive_path.split("/")[-1]
        name = file.split(".")[0]
        path = "/data/web_static/releases/{}/".format(name)
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(path))
        run("tar -xzf /tmp/{} -C {}".format(file, path))
        run("rm /tmp/{}".format(file))
        run("mv {}web_static/* {}".format(path, path))
        run("rm -rf {}web_static".format(path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(path))
        return True
    except Exception:
        return False
