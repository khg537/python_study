#!/bin/python3

1. command 처리 예제
import subprocess

cmd = "ls -l"
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
out = out.decode("utf-8")
print(out)

