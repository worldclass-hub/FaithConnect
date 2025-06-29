#!/bin/bash

# Let gunicorn read the port from the environment using Python
PORT=${PORT:-8000}
exec gunicorn doxcela.wsgi:application --bind 0.0.0.0:$PORT
