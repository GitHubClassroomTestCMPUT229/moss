#!/usr/bin/env python

import subprocess
import sys
import os

# Python script to submit the code from a lab in CMPUT229 to be evaluated by moss.
#   - determines which lab by first cmdline argument
#   - gathers base code from ./<lab>/instructor/ if "-b" provided on commandline
#   - submits all student code from the lab directory ./<lab>/
#   - submits the base code to be omitted
#
# Usage: ./mossPython.py <dir> <base_flag>

def callScript(project_dir, base):
    #-------------------------------------------------------------------
    # Setup
    #-------------------------------------------------------------------
    base_dir = "instructor"
    # Clear old base file if it exists; mossScript will build a new one
    if os.path.isfile("./{}/{}/base.s".format(project_dir, base_dir)):
        os.remove("./{}/{}/base.s".format(project_dir, base_dir))

    # Invoke the mossScript
    if base:
        subprocess.call(["mossScript", "-d", "{}".format(project_dir), "-b"])
    else:
        subprocess.call(["mossScript", "-d", "{}".format(project_dir)])

def main(project_dir, base):
    call_script(project_dir, base)

if __name__ == "__main__":
    assert len(argv) >= 2
    assert len(argv) < 4
    project_dir = argv[1]
    base = False
    if len(argv) == 3:
        if argv[2] == "-b":
            base = True
    main(project_dir, base)
