#! /bin/bash

pip install PyGithub
export labelName=`python scripts/python/set-label-name.py $GHToken`
python scripts/python/set-label-name.py $GHToken
labelName=$(python scripts/python/set-label-name.py $GHToken $GHToken)
export labelName=$labelName

