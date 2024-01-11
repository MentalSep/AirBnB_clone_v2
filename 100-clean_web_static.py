#!/usr/bin/python3
"""Module for web app deployment"""
from fabric.api import put, run, env, local, cd, lcd
import os

env.hosts = ['18.204.14.56', '35.153.226.169']


def do_clean(number=0):
    """clean up old versions"""
    number = int(number)
    if number == 0:
        number = 1

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
