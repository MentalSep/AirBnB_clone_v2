#!/usr/bin/python3
"""Module for web app deployment"""
from fabric.api import put, run, env, local
from os.path import exists
from datetime import datetime

env.hosts = ['18.204.14.56', '35.153.226.169']


def do_clean(number=0):
    """clean up old versions"""
    if number == 0 or number == 1:
        local("cd versions; ls -t | tail -n +2 | xargs rm -rf")
        run("cd /data/web_static/releases; ls -t | tail -n +2 | xargs rm -rf")
    else:
        local("cd versions; ls -t | tail -n +{} | xargs rm -rf".format(number))
        run("cd /data/web_static/releases; ls -t | tail -n +{} | xargs rm -rf".
            format(number))
