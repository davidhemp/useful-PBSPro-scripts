#!/usr/bin/env python3
import subprocess
from collections import defaultdict
import re

nodes = defaultdict(lambda: {"state": "Unknown", "queues": []})

# Get the list of all nodes and their state from 
running_subjobs = subprocess.check_output(["pbsnodes", "-aF", "dsv"]).decode().strip().split("\n")

for line in running_subjobs:
    node, state, Qlist = None, None, ""
    for element in line.split("|"):
        if element.startswith("Name"):
            node = element.split("=")[1].strip().split(".")[0]
        if element.startswith("state"):
            state = element.split("=")[1].strip()
        if element.startswith("resources_available.Qlist"):
            Qlist = element.split("=")[1].strip()
    if node:
        for Q in Qlist.split(","):
            nodes[node]["queues"].append(Q)
        nodes[node]["state"] = state
    else:
        print("Missing information for node. Skipping")
        print(line)
