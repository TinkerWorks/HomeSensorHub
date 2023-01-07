#!/bin/bash

HOST=$1
PROJECT=$(basename $(pwd))
PACKAGE=$(dirname $(ls */__main__.py))

rsync -rPv --delete "$(pwd)/" $HOST:~/${PROJECT}/

case "$2" in
    "req")
        ssh -t "${HOST}" pip3 install -r /home/$USER/${PROJECT}/tests/requirements.txt
        ssh -t "${HOST}" pip3 install -r /home/$USER/${PROJECT}/requirements.txt
        ;;
    "main")
        ssh -t "${HOST}" "cd ${PROJECT} ; python3 -m ${PACKAGE}"
        ;;
    "test")
        ssh -t "${HOST}" "cd ${PROJECT} ; nose2-3 "
        ;;
    "install")
        ssh -t ${HOST} "cd ${PROJECT} ; python3 -m pip install --upgrade --user --verbose ."
        ;;
    "copy")
        echo "Just copy and done"
        ;;
    *)
        exit 4
        ;;
esac
