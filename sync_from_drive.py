#!/usr/bin/env python

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


args = docopt(__doc__.format(self_filename=os.path.basename(__file__)))
source_dir = args['<usb_key_path>']

assert os.path.exists(source_dir) and os.path.isdir(source_dir)
# Check files
regexp = r'zim-notes_\d{8}(.*)?\.[tgz,tar\.gz]'
backup_files = search_file(regexp, source_dir)
assert backup_files, "Backup file not found in {}: {}".format(source_dir, regexp)
usb_backup_filepath = sorted(backup_files, reverse=True)[0]  # Use newest one
# Backup zim
print("=> Backup zim ...")
## compress Zim dir
assert os.path.exists(os.path.expanduser("~/zim-notes"))
local_tgz_filepath = "~/zim-notes_{}.tgz".format(datetime.datetime.now().strftime('%Y%m%d'))
shell("tar cf {}  -C {} zim-notes".format(local_tgz_filepath, os.path.expanduser("~/")))
assert os.path.exists(os.path.expanduser(local_tgz_filepath)) and os.path.getsize(os.path.expanduser(local_tgz_filepath)) > 0
# Kill zim
print("=> Kill zim ...")
killall_zim()
# Restore zim
shutil.rmtree(os.path.expanduser("~/zim-notes"))
print("=> Restore zim (using '{}')".format(usb_backup_filepath))
shell("tar xf {} -C {}".format(usb_backup_filepath, os.path.expanduser("~")))
# # print("=> update dotfiles")
# subprocess.call("git pull", shell=True, cwd=os.path.expanduser("~/dev/dotfiles/"))
print("=> end")