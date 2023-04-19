#!/usr/bin/env python3
import subprocess
from collections import defaultdict
import re

"""
 If anyone knows a better way to interact with PBS let me know. This returns 2 lines per subjob, for example:
6370363[88].pbs rz619    v1_mediu submit_6Q_ 232547   1 250   50gb 72:00 R 05:53
   Job run at Fri Jan 06 at 05:45 on (cx3-5-21.cx3.hpc.ic.ac.uk:ncpus=250:...
6610113[1524].p tjw19    v1_throu agreement_ 682601   1   8   90gb 72:00 R 14:11
   Job run at Thu Jan 05 at 21:26 on (cx3-1-16.cx3.hpc.ic.ac.uk:ncpus=8:me...
"""
running_subjobs = subprocess.check_output(["qstat", "-t", "-r", "-s"]).decode().strip().split("\n")[4:]

if len(running_subjobs)%2 != 0:
        raise ValueError("Expected an even number of lines from qstat")

subjobs_per_user = defaultdict(lambda: {"cx1":0, "cx2":0, "cx3":0, "hx1":0 })
for i in range(0, len(running_subjobs), 2):
        # Assume only subjobs has a square bracket in jobid
        if running_subjobs[i].find("[")  > -1:
                user=running_subjobs[i].split()[1]
                node_type = re.search("[c,h]x[0-3]", running_subjobs[i+1]).group()
                subjobs_per_user[user][node_type] += 1

print("{:10}  {:4} {:4} {:4} {:4} {:4}".format("user", "cx1", "cx2", "cx3", "hx1", "Total"))
for user, jobs in subjobs_per_user.items():
        print("{:10} {:4} {:4} {:4} {:4} {:6}".format(user, jobs["cx1"], jobs["cx2"], jobs["cx3"], jobs["hx1"], sum(jobs.values())))

