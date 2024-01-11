#!/usr/bin/python3
"""Module for web app deployment"""
from fabric.api import put, run, env, local
from os.path import exists
from datetime import datetime

env.hosts = ['18.204.14.56', '35.153.226.169']


def do_clean(number=0):
    """clean up old versions"""
    number = int(number)
    if number < 0:
        return
    if number == 0:
        number = 1
    local("ls -d -1tr versions/* | tail -n +{} | \
          xargs -d '\n' rm -f --".format(number + 1))
    run("ls -d -1tr /data/web_static/releases/* | tail -n +{} | \
        xargs -d '\n' rm -rf --".format(number + 1))
