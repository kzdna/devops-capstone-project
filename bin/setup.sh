#!/bin/bash
echo "Installing dependencies..."
pip3 install --user flask flask-sqlalchemy flask-talisman flask-cors gunicorn nose
echo "Setup complete!"
