#!/bin/bash
pbsnodes -l | grep -v "DECOMM" | grep -v "ADMIN"
