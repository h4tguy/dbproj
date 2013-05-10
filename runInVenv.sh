#!/bin/bash
cd `dirname $0`
set -e
if [ ! -d venv ]; then
    ./setup.sh
fi
source venv/bin/activate
python runserver.py
