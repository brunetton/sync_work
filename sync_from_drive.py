#!/usr/bin/env python

"""
Sync from usb key => computer
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


args = docopt(__doc__.format(self_filename=os.path.basename(__file__)))
source_dir = args['<usb_key_path>']

assert os.path.exists(source_dir) and os.path.isdir(source_dir)
# Check files
backup_files = search_file('zim-notes_\d{8}\.[tgz,tar\.gz]', source_dir)
assert backup_files, "Backup file not found in {}: {}".format(source_dir, regexp)
zim_tgz_path = sorted(backup_files, reverse=True)[0]  # Use newest one
# Backup zim
print("=> Backup zim ...")
## compress Zim dir
assert os.path.exists(os.path.expanduser("~/zim-notes"))
tgz_filepath = "~/zim-notes_{}.tgz".format(datetime.datetime.now().strftime('%Y%m%d'))
shell("tar cf {}  -C {} zim-notes".format(tgz_filepath, os.path.expanduser("~/")))
assert os.path.exists(os.path.expanduser(tgz_filepath)) and os.path.getsize(os.path.expanduser(tgz_filepath)) > 0
shutil.rmtree(os.path.expanduser("~/zim-notes"))
# Restore zim
print("=> Restore zim (using '{}')".format(zim_tgz_path))
shell("tar xf {} -C {}".format(tgz_filepath, os.path.expanduser("~")))
# # print("=> update dotfiles")
# subprocess.call("git pull", shell=True, cwd=os.path.expanduser("~/dev/dotfiles/"))
print("=> end")