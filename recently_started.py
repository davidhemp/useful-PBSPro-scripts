#!/usr/bin/env python3
# A script to find the details of the jobs that started in a given time period
import json
from datetime import datetime, timedelta
import subprocess

def get_test_data():
    """ For testing, needs to be moved to unit test"""
    # Load as bytes so we can drop charaters that aren't utf-8
    with open("test_data/queue_json", "rb") as f:
        raw_data = f.read().decode("utf-8", errors="ignore")

def load_json_data(raw_data):
    # Drop lines that contain BASH_FUNC
    data = []
    for line in raw_data.splitlines():
        if "BASH_FUNC" in line:
            new_line = '"BASH_FUNC": "Droped"'  # Drop the line
            if line.endswith(","):
                new_line += ","
            line = new_line
        data.append(line)
    #Convert back to string so it can be loaded as json
    data = "".join(data)
    json_data = json.loads(data, strict=False)
    return json_data

if __name__ == "__main__":
    raw_data = subprocess.check_output(["qstat", "-t", "-f", "-F", "json"]).decode("utf-8", errors="ignore")
    json_data = load_json_data(raw_data)

    #Get jobs that started an hour ago
    now = datetime.now()
    time_delta = timedelta(hours=1)
    for jobid, job in json_data["Jobs"].items():
        if job["job_state"] == "R" or job["job_state"] == "E":
            # convert stime to timestamp
            #'Wed Apr 19 08:39:36 2023'
            try:
                stime_str = job["stime"]
            except KeyError:
                print ("No stime for jobid: {}".format(jobid))
                continue
            stime = datetime.strptime(stime_str, "%a %b %d %H:%M:%S %Y")
            time_diff = now - stime
            if time_diff < time_delta:
            print(jobid, job["Job_Owner"], job["exec_host"])
