#!/usr/bin/python

# Usage: ./pywatch.py <path> [-d]
# path is location of your python code which you want
# -d is optional argument which prints python file that changed
# to monitor for changes.

# Example:
# Throw this script in the home directory of your
# ERPNext server and run
#./pywatch frappe-bench/apps/ &

# Only dependency for this script is pyinotify. To install it
# run "sudo pip install pyinotify" (and if you don't want to
# install it globally, it's recommended to use python
# virtual environment (http://docs.python-guide.org/en/latest/dev/virtualenvs/)

# Explanation:
# While testing code on a Frappe Production setup, modifications
# of python code inside an app don't take effect until you run
# "bench restart", which usually takes around 10-13 seconds.
# We discovered that by killing gunicorn (pkill gunicord), the
# python code gets reloaded and gunicorn process gets
# restarted almost instantly.
# 
# This script watches for changes in python files and
# automatically triggers gunicord restart whenever a
# python file changes. This speeds up development
# process and makes it possible to modify python code
# in production without 13 second downtime caused by
# running "bench restart".

# Note that this script isn't necessary in Development
# Setup of bench, and only applies to Production version.

# TODO:
#  -possibly exclude .git directory with exclude_filter
#  -add a timer and don't kill gunicorn more than once every second.
#  -Issue: when modifying python with vim, on_event is called twice.
#  -Check what happens when a bunch of python files get changed at the same time, for example when installing new app.

import time, sys, pyinotify, subprocess

debug = False

if len(sys.argv) != 2:
   if len(sys.argv) == 3 and sys.argv[2] == '-d':
      debug = True
   else:
      print('%s <PATH_TO_MONITOR> [-d]' % sys.argv[0])
      exit()

path = sys.argv[1]

wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm)

def on_event(arg):
   name = arg.pathname
   #print('event %s' % name)
   if name.split('.')[-1] == 'py':
      if debug:
         print('python file changed: %s' % name)
      subprocess.call(['pkill', 'gunicorn'])

#watch_mask = pyinotify.ALL_EVENTS
watch_mask = pyinotify.IN_CREATE | pyinotify.IN_MODIFY
#exclude_filter=not_py_file (this can be used to exclude .git directory)
wm.add_watch(path, watch_mask, proc_fun=on_event, rec=True, auto_add=True, quiet=False)

notifier.loop()

