import sys
import os.path
import shutil
import smtplib
import json

from email.mime.text import MIMEText
from git import Repo
from mossPython import callScript as submit_repos

#------------------------------------------------------------------------------
# Opens ./teachingTeam.json and returns the contacts list for the teaching team
# contacts["contacts"] is a list of email addresses: ["<address1>", "<address2>", ... ]
#------------------------------------------------------------------------------
def get_contacts():
    f = open("teachingTeam.json", "r")
    contacts = json.load(f)
    return contacts["contacts"]

#------------------------------------------------------------------------------
# Opens a teams.json file pointed to by path and returns a dictionary representing the teams.
# Includes the instructor's base code as a team, since handling this repo's code is the same.
# teams is a dict like:
#   {<team>: {<lab>: <repo_url>, <lab>: <repo_url>, ...}, <team>: {<lab>: <repo_url>, <lab>: <repo_url>, ...}, ... }
#------------------------------------------------------------------------------
def parse_teams(path):
    f = open(path, "r")
    teams = json.load(f)
    return teams

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
#------------------------------------------------------------------------------
# Sends an email notifying about similarities to all members of the teaching team.
# https://docs.python.org/2/library/email-examples.html
# TODO: Serve the html as html within the email.
# TODO: Permit sending from server on eg: Heroku
# https://medium.freecodecamp.com/send-emails-using-code-4fcea9df63f
# https://www.ualberta.ca/computing-science/links-and-resources/technical-support/email/authenticated-smtp
#------------------------------------------------------------------------------
def notify(lab):
    fp = open("./{}/results.html".format(lab), 'rb')
    msg = MIMEText(fp.read())
    fp.close()

    sender = "hoye@cs.ualberta.ca"
    contacts = get_contacts()
    for contact in contacts:
        msg['Subject'] = "CMPUT 229 {} Results".format(lab)
        msg['From'] = sender
        msg['To'] = contact

        s = smtplib.SMTP('localhost')
        # Rough-in of authentication.  Invalid auth error. USERNAME & PASSWORD omitted for now.
        # s = smtplib.SMTP('smtp-auth.cs.ualberta.ca', 587)
        # s.starttls()
        # s.login(USERNAME, PASSWORD)
        s.sendmail(sender, contact, msg.as_string())
        s.quit()

#------------------------------------------------------------------------------
# Parameters:
#   lab:    string used to identify which lab is being pulled
#   teams:  dict used to map lab & team to a specific repo
# Effect:
#   Repos are cloned into ./<labID>/<teamID>/
#------------------------------------------------------------------------------
def get_repos(lab, teams):
    print "Gathering repos for moss"
    for team in teams.keys():
        if teams[team][lab]:
            clone_path = "./{}/{}/".format(lab, team)
            print "Cloning into " + clone_path
            if os.path.exists(clone_path):
                shutil.rmtree(clone_path)
            Repo.clone_from(teams[team][lab], clone_path)

#------------------------------------------------------------------------------
# lab1 tests when instructor provides no base code
# lab2 tests when instructor does provide base code
# lab3 tests when a student has an empty repo at the deadline
# lab4 tests source code mishmashed from lab1 source code with no base code
# lab5 tests source code mishmashed from lab1 source code with base code present
#------------------------------------------------------------------------------
def test():
    teams = parse_teams("./test/teams.json")
    labs = teams["instructor"].keys()
    for lab in labs:
        get_repos(lab, teams)
        submit_repos(lab, teams["instructor"][lab])
        notify(lab)
    
#------------------------------------------------------------------------------
# Parameter:
#   lab: string to identify which lab is being processed.
#        can be passed in on commandline if cron job command, or can be passed in by python process
# Effect:
#   Student repos for the lab are gathered locally
#   Instructor's base code is gathered locally
#   mossScript.py is invoked as submit_repos
#   the resulting .html file is captured and emailed to the teaching team
#   TODO: Get Noah's wget process to gather html & references within
#   TODO: Work on email authentication
#------------------------------------------------------------------------------
def mossService(lab):
    teams = parse_teams("./teams.json")
    get_repos(lab, teams)
    submit_repos(lab, teams["instructor"][lab])
    notify(lab)

def main(argv):
    if len(argv) != 2:
        print("Usage: python moss.py <lab> OR python moss.py test")
    if len(argv) > 1:
        if argv[1] == "test":
            test()
        elif argv[1] == "clear":
            clear()
        else:
            lab = argv[1]
            mossService(lab)

if __name__ == "__main__":
    main(sys.argv)

