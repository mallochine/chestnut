#!/usr/bin/bash

python ~/.chestnut/from_cli.py $@
wait

readarray lines < $HOME"/.chestnut/tmp_cmds.txt"
for line in "${lines[@]}";
do
    $line
done
