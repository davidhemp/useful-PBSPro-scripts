#!/bin/bash
# Returns a list of nodes and their resources that are currently not running any jobs. 
pbsnodes -aSj | grep "\-\-$" | grep free
