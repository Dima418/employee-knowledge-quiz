#!/bin/bash

if [ -d "env" ] || [ -d "venv" ] || [ -d "virtualenv" ]
then
    echo "Python virtual environment exists." 
else
    python3 -m venv venv
fi

source venv/bin/activate

pip3 install -r requirements.txt