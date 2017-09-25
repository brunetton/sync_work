#!/usr/bin/env python

"""
Sync from computer => usb key
Usage:
	 {self_filename} <usb_key_path>
"""

import argparse
import datetime
import os
import re
import shutil

from docopt import docopt

from sync_utils import *


NOTEBOOKS_PATH = os.path.expanduser("~/dev/dbnomics/notebooks/")

args = docopt(__doc__.format(self_filename=os.path.basename(__file__)))
dest_path = args['<usb_key_path>']

assert os.path.exists(os.path.expanduser("~/zim-notes"))
assert os.path.exists(dest_path) and os.path.isdir(dest_path)
assert os.path.exists(NOTEBOOKS_PATH) and os.path.isdir(NOTEBOOKS_PATH)
# Check if backup file exists
today_backup_filename = "zim-notes_{}.tgz".format(datetime.datetime.now().strftime('%Y%m%d'))
today_backup_filepath = os.path.join(os.path.expanduser("~/"), today_backup_filename)
if os.path.exists(today_backup_filepath):
    # add timestamp to filename
    today_backup_filename = "zim-notes_{}.tgz".format(datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
    today_backup_filepath = os.path.join(os.path.expanduser("~/"), today_backup_filename)
    assert not os.path.exists(today_backup_filepath)
# Backup to drive
print "=> backup to {}".format(today_backup_filepath)
shell("tar cf {}  -C {} zim-notes".format(today_backup_filepath, os.path.expanduser("~/")))
assert os.path.exists(today_backup_filepath) and os.path.getsize(today_backup_filepath) > 0
# Backup to usb drive
today_usb_backup_filepath = os.path.join(dest_path, today_backup_filename)
assert not os.path.exists(today_usb_backup_filepath), "{} already exists".format(today_usb_backup_filepath)
print "=> backup to {}".format(today_usb_backup_filepath)
shutil.copy2(today_backup_filepath, today_usb_backup_filepath)
assert os.path.exists(today_usb_backup_filepath) and os.path.getsize(today_usb_backup_filepath) > 0

# Notebooks
noteboooks_dest_path = os.path.join(dest_path, 'notebooks')
print "=> Copying notebooks to {}".format(dest_path)
assert not os.path.exists(noteboooks_dest_path)
shutil.copytree(NOTEBOOKS_PATH, noteboooks_dest_path)

print("=> end")