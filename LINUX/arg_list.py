#!/usr/bin/python

import os
import subprocess
import sys

def get_cmd_output(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    out=out.rstrip("\n")
    return out

out = get_cmd_output("ls -l")


if __name__ == '__main__':
    arg_list = sys.argv
    print(arg_list)
