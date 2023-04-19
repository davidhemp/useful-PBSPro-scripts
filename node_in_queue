#!/bin/bash

if [[ ! $1 ]] ; then
        pbsnodes -a | grep "Mom\|Qlist"
else
  pbsnodes -a | grep "Mom\|Qlist" | grep -B 1 $1
fi

