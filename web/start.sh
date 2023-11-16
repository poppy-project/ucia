#!/bin/bash

cd ~/rosa-master/web

/home/pi/.local/bin/gunicorn -w 2 wsgi:app -b 0.0.0.0:8000