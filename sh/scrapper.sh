#!/bin/bash

sudo redis-server /home/pi/programming/datascrapper/src/db/redis.conf

python datascrapper/src/slug.py
