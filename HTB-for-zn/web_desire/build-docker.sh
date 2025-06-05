#!/bin/sh
docker build --build-arg FLAG=HTB{$(openssl rand -hex 32)} --tag=web-desires .