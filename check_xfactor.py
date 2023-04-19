#!/usr/bin/env python3
from datetime import datetime
import os

#import matplotlib.pyplot as plt

def get_task_list():
    """Get the last 14 days of accounting logs"""
    return sorted(os.listdir("/home/PBS_LOGS/pbs_accounting"))[-14:]

def process_day(data):
    for line in data:
        if "S" in line.split("pbs")[0] and "[]" not in line.split("pbs")[0]:
            # Dumb but much faster than regex
            queue = line.split("queue")[1].split(" ")[0][1:]
            if queue[:2] == "v1":
                qtime = int(line.split("qtime=")[1].split(" ")[0])
                stime = int(line.split("start=")[1].split(" ")[0])
                walltime = [ int(x) for x in line.split("Resource_List.walltime=")[1].split(" ")[0].split(":")]
                walltime_secs = walltime[0] * 3600 + walltime[1]*60 + walltime[2]
                if walltime_secs > 60:
                    xfactor=(stime-qtime)/walltime_secs
                    if queue in all_queues.keys():
                        all_queues[queue].append(xfactor)
                    else:
                        all_queues[queue] = [xfactor]
    return

all_queues = {}
files = get_task_list()
for day in files:
    day_data = "/home/PBS_LOGS/pbs_accounting/" + day
    with open(day_data) as f:
        data = f.read().split("\n")
        process_day(data)

print("Queue\t\t\tMean xfactor\tMax xfactor")
print("----------------------------------------")
for queue, values in all_queues.items():
    print(f"{queue.ljust(14)}\t\t {sum(values)/len(values):.6f} \t {max(values):.6f}")


