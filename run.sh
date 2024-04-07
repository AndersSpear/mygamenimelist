#!/bin/bash
source /home/ta/mysongnimelist/venv/bin/activate
cd /home/ta/mysongnimelist
export SPOTIPY_CLIENT_ID='43c32308e1f940cba0cbcda5c0ecb6d6'
export SPOTIPY_CLIENT_SECRET='43d5d1c9c3a94bfda31ca4728ab2fed5'
export DISCORD_CLIENT_ID='1101288251232358430'
export DISCORD_CLIENT_SECRET='WW-M3OXs44pxQwycvfhcC-OyiQjYKHRC'
waitress-serve --port 5001 --call "flask_app:create_app"
