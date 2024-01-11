#!/usr/bin/python3
"""Module for web app deployment"""
from fabric.api import put, run, env, local
from os.path import exists
from datetime import datetime

env.hosts = ['18.204.14.56', '35.153.226.169']


def do_pack():
    """compress the web_static files to .tgz"""
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file = "versions/web_static_{}.tgz".format(date)
    if local("tar -cvzf {} web_static".format(file)).succeeded:
        return file
    else:
        return None


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


def deploy():
    """creates and distributes an archive to your web servers"""
    arch_path = do_pack()
    if arch_path is None:
        return False
    return do_deploy(arch_path)
