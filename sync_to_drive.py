#!/usr/bin/env python3

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
ZIM_PATH = os.path.expanduser("~/zim-notes/")

args = docopt(__doc__.format(self_filename=os.path.basename(__file__)))
dest_path = args['<usb_key_path>']

assert os.path.exists(os.path.expanduser("~/zim-notes"))
assert os.path.exists(dest_path) and os.path.isdir(dest_path)
assert os.path.exists(NOTEBOOKS_PATH) and os.path.isdir(NOTEBOOKS_PATH)

def backup(source_file_or_dir, local_backup_path, dest_backup_path):
    """ - make file-timestamp.tgz on local_backup_path
        - copy this backup to dest_backup_path
    All paths can be with "~"
    """
    assert os.path.exists(source_file_or_dir)
    assert os.path.exists(dest_backup_path) and os.path.isdir(dest_backup_path)
    print("=> Backup {}".format(source_file_or_dir))
    # expanduser
    source_file_or_dir = os.path.expanduser(source_file_or_dir)
    local_backup_path = os.path.expanduser(local_backup_path)
    dest_backup_path = os.path.expanduser(dest_backup_path)
    # Check if backup file exists
    source_filename = os.path.basename(os.path.normpath(source_file_or_dir))
    today_backup_filename = "{}_{}.7z".format(source_filename, datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
    today_backup_filepath = os.path.join(local_backup_path, today_backup_filename)
    assert not os.path.exists(today_backup_filepath)
    # Backup to dest
    shell("7z a {} {}".format(today_backup_filepath, source_file_or_dir), capture_output=True)
    assert os.path.exists(today_backup_filepath) and os.path.getsize(today_backup_filepath) > 0
    # Backup to dest
    dest_backup_filepath = os.path.join(dest_path, today_backup_filename)
    assert not os.path.exists(dest_backup_filepath), "{} already exists".format(dest_backup_filepath)
    print("  - backup to {}".format(dest_backup_filepath))
    shutil.copy2(today_backup_filepath, dest_backup_filepath)
    assert os.path.exists(dest_backup_filepath) and os.path.getsize(dest_backup_filepath) > 0

# Zim
backup(ZIM_PATH, "~", dest_path)
# Notebooks
backup(NOTEBOOKS_PATH, "~", dest_path)

print("=> end")