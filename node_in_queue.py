#!/usr/bin/env python3
import subprocess
from collections import defaultdict
import sys

def all_nodes() -> dict:
    """Return a dictionary of all nodes and their state"""
    nodes = defaultdict(lambda: {"state": "Unknown", "queues": []})
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
    return nodes


if __name__ == "__main__":
    nodes = all_nodes()
    if len(sys.argv) == 1:
        for node, info in nodes.items():
            print(f"{node}: {info['state']} {info['Qlist']}")
    elif len(sys.argv) == 2:
        target_queue = sys.argv[1]
        for node, info in nodes.items():
            if target_queue in info["Qlist"]:
                print(f"{node}: {info['state']} {info['Qlist']}")  
    elif len(sys.argv) > 2:
        print("Usage: node_in_queue.py [queue]")
        sys.exit(1)