#!/usr/bin/bash

python ~/.chestnut/from_cli.py $@
wait

source $HOME"/.chestnut/tmp/cmds.txt"
