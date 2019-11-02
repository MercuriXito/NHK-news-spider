#/bin/python3

import sys,os
from config.configuration import pconfig
from datetime import datetime

cons = pconfig()

projectcon = cons.get_config()["project-config"]
propath = projectcon["project_abspath"]

# config works
workers = 4

# log file of gunicorn
logdir = propath + "/" + projectcon["logdir"]

if not os.path.exists(logdir):
    os.mkdir(logdir)

accesslog = logdir + "/" + "gunicorn_access.log"
errorlog = logdir + "/" + "gunicorn_error.log"
pidfile = logdir + "/" + "gunicorn.pid"

capture_output = True

for file in [accesslog, errorlog]:
    with open(file,"a") as f:
        f.write("Start logger in {}\n".format(datetime.now()))

# bind configuration
bind = "127.0.0.1:8989 "
