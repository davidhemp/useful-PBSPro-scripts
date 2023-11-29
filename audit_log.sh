#!/bin/bash

LOG_FILES=$(ls /var/spool/pbs/server_logs/ | tail)
grep $1 $LOG_FILES | grep -v "Type [0,21,95,19]" 
