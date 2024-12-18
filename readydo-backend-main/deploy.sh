#!/bin/bash

. ./venv/bin/activate

pip3 install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "pip3 install failed"
    exit 1
fi

python3 manage.py migrate
if [ $? -ne 0 ]; then
    echo "Migrate failed"
    exit 1
fi

python3 manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
    echo "Collect static failed"
    exit 1
fi

sudo service supervisor restart

sudo systemctl restart gunicorn
