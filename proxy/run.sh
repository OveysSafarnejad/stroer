#!/bin/sh

set -e

envsubst < /etc/nginx/conf.d/default.conf.tpl > /etc/nginx/conf.d/default.conf 

# run nginx in docker container as a forground app (not in background)
nginx -g 'daemon off;'
