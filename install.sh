#!/bin/bash

# Installation script for Practical 1
# Must be ran as sudo

# Prepereqs for python modules
apt-get install sqlite3
apt-get install pip
apt-get install apache2-utils

# Python modules
pip install flask
pip install requests
pip install sqlalchemy
pip install flask-sqlalchemy
pip install sqlalchemy-migrate
