#!/usr/bin/python3
"""Module for web app deployment"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """compress the web_static files to .tgz"""
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file = "versions/web_static_{}.tgz".format(date)
    if local("tar -cvzf {} web_static".format(file)).succeeded:
        return file
    else:
        return None
