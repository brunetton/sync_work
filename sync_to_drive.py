#!/usr/bin/env python3

"""
Sync from computer => usb key
Usage:
	 {self_filename} <usb_key_path>
"""

import datetime
import os
import shutil

from docopt import docopt

from sync_utils import *
import sync_work_constants


def backup(source_file_or_dir, dest_backup_path):
    """ - make file-timestamp.tgz on ~
        - copy this backup to dest_backup_path
    (all paths can contain "~" char)
    """
    assert os.path.exists(source_file_or_dir)
    assert os.path.exists(dest_backup_path) and os.path.isdir(dest_backup_path)
    print("=> Backup {}".format(source_file_or_dir))
    home_path = os.path.expanduser("~")
    # expanduser
    source_file_or_dir = os.path.expanduser(source_file_or_dir)
    dest_backup_path = os.path.expanduser(dest_backup_path)
    # Check backup file doesn't exists
    source_filename = os.path.basename(os.path.normpath(source_file_or_dir))
    today_backup_filename = "{}_{}.7z".format(source_filename, datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
    today_backup_filepath = os.path.join(home_path, today_backup_filename)
    assert not os.path.exists(today_backup_filepath)
    # Backup to local
    relative_source_path = os.path.relpath(source_file_or_dir, home_path)  # "/home/bruno/dev/dbnomics/notebooks/ => dev/dbnomics/notebooks/"
    shell("cd ~; 7z a {} {}".format(today_backup_filename, relative_source_path), capture_output=True)
    assert os.path.exists(today_backup_filepath) and os.path.getsize(today_backup_filepath) > 0
    # Backup to dest
    dest_backup_filepath = os.path.join(dest_path, today_backup_filename)
    assert not os.path.exists(dest_backup_filepath), "{} already exists".format(dest_backup_filepath)
    print("  - backup to {}".format(dest_backup_filepath))
    shutil.copy2(today_backup_filepath, dest_backup_filepath)
    assert os.path.exists(dest_backup_filepath) and os.path.getsize(dest_backup_filepath) > 0



args = docopt(__doc__.format(self_filename=os.path.basename(__file__)))
dest_path = args['<usb_key_path>']

assert os.path.exists(os.path.expanduser("~/zim-notes"))
assert os.path.exists(dest_path) and os.path.isdir(dest_path)
stuff_to_sync = sync_work_constants.STUFF_TO_SYNC
for stuff_path in stuff_to_sync:
    assert os.path.exists(os.path.expanduser(stuff_path)) and os.path.isdir(os.path.expanduser(stuff_path)), \
            "Error: not found or not a dir {}".format(stuff_path)  # for now, check dirs as single files not really tested

for stuff_path in stuff_to_sync:
    backup(os.path.expanduser(stuff_path), dest_path)


print("=> end")