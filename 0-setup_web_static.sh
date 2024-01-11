#!/usr/bin/env bash
# Script that sets up the web servers for the deployment of web_static
apt-get update
apt-get -y install nginx

mkdir -p /data/web_static/releases/test/ /data/web_static/shared/
echo "Testing!" > /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data/

sed -i "/listen 80 default_server;/a location /hbnb_static/ { alias /data/web_static/current/;}" /etc/nginx/sites-available/default

service nginx restart
