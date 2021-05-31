#! /bin/bash

pip3 install PyGithub
export labelName=`python3 scripts/python/set-label-name.py $GHToken`
