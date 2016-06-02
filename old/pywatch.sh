#!/bin/bash

#BROKEN FILE: DO NOT USE THIS!!!
echo "BROKEN FILE: DO NOT USE THIS SCRIPT!!!"
exit 1

#install sudo apt-get install inotify-tools realpath

if [ -z $1 ]; then
    echo "USAGE: $0 <path to python sources>";
    exit 1
fi

SRC=$(realpath $1)

echo "Watching: $SRC"

#while RES=($(inotifywait -r -q -e modify,attrib,move,close_write,create,delete,delete_self $SRC)); do
while RES=($(inotifywait -r -q -e modify $SRC)); do
    DIR=${RES[0]}
    EVENT=${RES[1]}
    FILE=${RES[2]}
    FILEPATH=${DIR}${FILE}
    COMPILE=1
    echo $FILE
    echo $FILEPATH

    if [ -f "$FILEPATH" ] && [[ $FILE =~ .py$ ]]; then
        echo "[$EVENT] $FILEPATH"
        ### BOF - ADD YOUR CUSTOM CODE HERE ###
        pkill gunicorn
        ### EOF - ADD YOUR CUSTOM CODE HERE ###

        echo " -------------------------------------"
    fi
done
