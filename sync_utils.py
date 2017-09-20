#!/usr/bin/env python

import subprocess


def shell(command, check_errors=True, cwd=None):
    errors = subprocess.call(command, shell=True, cwd=cwd)
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
