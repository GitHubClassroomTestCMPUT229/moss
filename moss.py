#!/usr/bin/env python

import sys
import os.path
import shutil
import smtplib
import json
import subprocess
from subprocess import Popen, PIPE, STDOUT

# Expects base code to be in ./<lab>/instructor/base/
# Want to handle more than just *.s; just concat. all *.* in /base/
def makeBase(lab, suffix = "s"):
    base_dir = "./{}/instructor/base/".format(lab)
    base_file = "./{}/instructor/base.{}".format(lab, suffix)
    # Clear old base file if it exists.
    if os.path.isfile(base_file):
        os.remove(base_file)
    # Build a base file
    files = os.listdir(base_dir)
    base = open(base_file, "w")
    for f in files:
        f = open("{}{}".format(base_dir, f), "r")
        base.write(f.read())
        f.close()
    base.close()
    return base_file

# Expects repos to be gathered.
# Base code to be in ./<lab>/instructor/base/
# Student submissions to be in ./<lab>/<team>/<submission>/
# Archived submissions to be in ./<lab>/archived/
def submitRepos(lab, base, lang="mips", suffix="s"):
    print "Submitting repos to moss."

    lab_dir = "./{}/*/submission/*.{}".format(lab, suffix)
    archived_dir = "./{}/archived/*.{}".format(lab, suffix)
    base_file = makeBase(lab)
    subprocess.call(["mossScript", 
                    "{}".format(lang),
                    "{}".format(base_file),
                    "{} {}".format(lab_dir, archived_dir)])

#------------------------------------------------------------------------------
# Clears all ./<lab>/ repos from cwd.
# Handy to tidy up after running the test and peeking at what gets pulled.
#------------------------------------------------------------------------------
def clear(lab=None):
    if lab == None:
        f = open("./teams.json", "r")
        teams = json.load(f)
        labs = teams["instructor"].keys()
        for lab in labs:
            shutil.rmtree("./{}/".format(lab))
    else:
        shutil.rmtree("./{}/".format(lab))

def copy_response(lab):
    f = open("./{}/results.html".format(lab), "r")
    out = open("./results/{}.html".format(lab), "w")
    out.write(f.read())
    f.close()
    out.close()

if __name__ == "__main__":
    submitRepos("testlab1", True)
    # main(sys.argv)

