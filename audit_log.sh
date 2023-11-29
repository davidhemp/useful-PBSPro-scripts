#!/bin/bash

LOG_PATH="/var/spool/pbs/server_logs/"
LOG_FILES=$(find $LOG_PATH -mtime -7)
grep $1 $LOG_FILES | grep -v "Type [0,21,95,19]" 
