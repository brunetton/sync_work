#!/usr/bin/env python

"""
Sync usb key => laptop
Usage:
	 {self_filename} <usb_key_path>
"""

import argparse
import datetime
import os
import re
import shutil
import subprocess

from docopt import docopt


def shell(command, check_errors=True, cwd=None):
    errors = subprocess.call(command, shell=True, cwd=cwd)
    if check_errors:
        assert not errors, errors


def search_file(regexp, dir):
    ''' find file in dir and return path. Raise error if not found or more than one file matchs'''
    found_filename = None
    for filename in os.listdir(dir):
        if re.search(regexp, filename):
            assert not found_filename, "Found multiple files matching {}".format(regexp)
            found_filename = filename
    assert found_filename, "File not found in {}: {}".format(dir, regexp)
    return os.path.join(dir, found_filename)


args = docopt(__doc__.format(self_filename=os.path.basename(__file__)))
source_dir = args['<usb_key_path>']

assert os.path.exists(source_dir) and os.path.isdir(source_dir)
# Check files
zim_tgz_path = search_file('zim-notes_\d{8}\.[tgz,tar\.gz]', source_dir)
# Backup zim
## kill
print("=> Backup zim ...")
for i in range(3):
    shell("killall zim; sleep 0.3", check_errors=False)
shell("killall zim -9", check_errors=False)
## Check killed
# assert subprocess.check_output("ps auxf|grep zim|grep -v 'grep'", shell=True) == ''
## tar gz
assert os.path.exists(os.path.expanduser("~/zim-notes"))
tgz_filepath = "~/zim_notes_{}.tgz".format(datetime.datetime.now().strftime('%Y%m%d'))
shell("tar cf {}  -C {} zim-notes".format(tgz_filepath, os.path.expanduser("~/")))
assert os.path.exists(os.path.expanduser(tgz_filepath)) and os.path.getsize(os.path.expanduser(tgz_filepath)) > 0
shutil.rmtree(os.path.expanduser("~/zim-notes"))
# Restore zim
print("=> Restore zim")
shell("tar xf {} -C {}".format(tgz_filepath, os.path.expanduser("~")))
