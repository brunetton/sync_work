#!/usr/bin/env python3

"""
Sync from usb key => computer
Usage:
     {self_filename} <usb_key_path>
"""

import datetime
import os
import shutil

from docopt import docopt

from sync_utils import *
import sync_work_constants


def restore(stuff_dest_path, source_path):
    stuff_dest_path = os.path.expanduser(stuff_dest_path)
    source_path = os.path.expanduser(source_path)
    stuff_name = os.path.basename(os.path.normpath(stuff_dest_path))
    home_path = os.path.expanduser("~")
    # Find archive
    regexp = stuff_name + '_(\d{8}-\d{6})\.7z'
    backup_files = search_file(regexp, source_path)
    assert backup_files, "Backup file not found in {}: {}".format(source_path, regexp)
    backup_filepath = sorted(backup_files, reverse=True)[0]  # Use newest one
    print("=> Restore {} (using {}) ...".format(stuff_name, backup_filepath))
    # Make local backup copy
    local_original_path = os.path.join(home_path, stuff_name)
    if os.path.exists(local_original_path):
        local_backup_filename = "{}_{}.7z".format(stuff_name, datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
        local_backup_filepath = os.path.join(home_path, local_backup_filename)
        relative_source_path = os.path.relpath(local_original_path, home_path)  # "/home/bruno/dev/dbnomics/notebooks/ => dev/dbnomics/notebooks/"
        shell("cd ~; 7z a {} {}".format(local_backup_filename, relative_source_path), capture_output=True)
        assert os.path.exists(local_backup_filepath) and os.path.getsize(local_backup_filepath) > 0, \
                "Error: local backup {} do not exists or is empty".format(local_backup_filepath)
    else:
        print("  -> not existing \"{}\", ignoring local backup".format(local_original_path))
    # Restore from source
    if os.path.exists(stuff_dest_path):
        shutil.rmtree(stuff_dest_path)
    shell("cd ~; 7z x {}".format(backup_filepath), capture_output=True)


args = docopt(__doc__.format(self_filename=os.path.basename(__file__)))
source_path = args['<usb_key_path>']

assert os.path.exists(source_path) and os.path.isdir(source_path)

# Kill zim
print("=> Kill zim ...")
killall_zim()

for stuff_dest_path in sync_work_constants.STUFF_TO_SYNC:
    restore(stuff_dest_path, source_path)

print("=> end")