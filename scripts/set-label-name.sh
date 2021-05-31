#! /bin/bash

pip install PyGithub
export labelName=`python scripts/python/set-label-name.py $GHToken`
