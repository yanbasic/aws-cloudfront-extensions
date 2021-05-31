#! /bin/bash

pip install PyGithub
python scripts/python/set-label-name.py $GHToken
export labelName=`python scripts/python/set-label-name.py $GHToken`
