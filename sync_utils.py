#!/usr/bin/env python3

import os
import re
import subprocess
from string import Template


class DeltaTemplate(Template):
    delimiter = "%"

def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    hours, rem = divmod(tdelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    d["H"] = '{:02d}'.format(hours)
    d["M"] = '{:02d}'.format(minutes)
    d["S"] = '{:02d}'.format(seconds)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)


def shell(command, check_errors=True, capture_output=False):
    if capture_output:
        errors = subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)
    else:
        errors = subprocess.call(command, shell=True)
    if check_errors:
        assert not errors, errors


def search_file(regexp, dir):
    '''Find files in dir matching given regexp and return a set of their paths'''
    found_filepaths = set()
    for filename in os.listdir(dir):
        if re.search(regexp, filename):
            found_filepaths.add(os.path.join(dir, filename))
    return found_filepaths


def killall_zim():
    for i in range(3):
        shell("killall zim; sleep 0.3", check_errors=False)
    shell("killall zim -9", check_errors=False)
    ## Check killed
    # assert subprocess.check_output("ps auxf|grep zim|grep -v 'grep'", shell=True) == ''
