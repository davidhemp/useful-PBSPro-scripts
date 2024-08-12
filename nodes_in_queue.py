#!/usr/bin/env python3
import subprocess
from collections import defaultdict
import sys

def all_nodes() -> dict:
    """Return a dictionary of all nodes and their state"""
    nodes = defaultdict(lambda: {"state": "Unknown", "Qlist": [], "comment": ""})
    running_subjobs = subprocess.check_output(["pbsnodes", "-aF", "dsv"]).decode().strip().split("\n")
    for line in running_subjobs:
        node, state, Qlist, comment = None, None, "", ""
        for element in line.split("|"):
            if element.startswith("Name"):
                node = element.split("=")[1].strip().split(".")[0]
            elif element.startswith("state"):
                state = element.split("=")[1].strip()
            elif element.startswith("resources_available.Qlist"):
                Qlist = element.split("=")[1].strip()
            elif element.startswith("comment"):
                comment = element.split("=")[1].strip()
        if node:
            for Q in Qlist.split(","):
                nodes[node]["Qlist"].append(Q)
                if "offline" in state:
                    nodes[node]["state"] = "offline"
                elif "down" in state:
                    nodes[node]["state"] = "down"
                else:
                    nodes[node]["state"] = state
            nodes[node]["comment"] = comment
        else:
            print("Missing information for node. Skipping")
            print(line)
    return nodes


if __name__ == "__main__":
    nodes = all_nodes()
    if len(sys.argv) == 1:
        for node, info in nodes.items():
            queues = ",".join(info["Qlist"])
            print(f"{node:<10}: {info['state']:<10} {queues:<20} {info['comment']}")  
    elif len(sys.argv) == 2:
        target_queue = sys.argv[1]
        for node, info in nodes.items():
            if target_queue in info["Qlist"]:
                queues = ",".join(info["Qlist"])[:40]
                print(f"{node:<12} {info['state']:<10} {queues:<40} {info['comment']}")  
    elif len(sys.argv) > 2:
        print("Usage: node_in_queue.py [queue]")
        sys.exit(1)