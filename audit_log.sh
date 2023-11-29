#!/bin/bash

LOG_PATH="/var/spool/pbs/server_logs/"
LOG_FILES=$(ls $LOG_PATH | tail)
grep $1 $LOG_PATH/$LOG_FILES | grep -v "Type [0,21,95,19]" 
