#!/bin/bash
for (( c=1; c<="$1"; c++ ))
do
        echo $c
        python manage.py jump_day
done