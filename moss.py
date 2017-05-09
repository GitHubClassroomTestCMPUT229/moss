from git import Repo
from mossPython import callScript as submit_repos
import sys
import os.path
import shutil
import smtplib
import json
# Import the email modules we'll need
from email.mime.text import MIMEText

#------------------------------------------------------------------------------
# https://docs.python.org/2/library/email-examples.html
#------------------------------------------------------------------------------
def notify(lab):
    fp = open("./{}/results.html".format(lab), 'rb')
    # Create a text/plain message
    # TODO: Serve the html as html within the email?
    msg = MIMEText(fp.read())
    fp.close()

    # me == the sender's email address
    me = "hoye@ualberta.ca"
    you = "hoye@ualberta.ca"
    # you == the recipient's email address
    msg['Subject'] = "CMPUT 229 {} Results".format(lab)
    msg['From'] = me
    msg['To'] = you

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    # TODO: Permit sending from server on eg: Heroku
    s = smtplib.SMTP('localhost')
    s.sendmail(me, [you], msg.as_string())
    s.quit()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def parse_teams(path):
    f = open(path, "r")
    teams = json.load(f)
    return teams

#------------------------------------------------------------------------------
# Requirements:
#   Team ids are stored in teams dict
#   Labs are at the next level of the dict
#   Accessing teams[teamID][LabID] return the GitHub url for the team's repo for that lab
# Parameter:
#   lab is used to identify which lab is being pulled
# Effect:
#   Repos are cloned into <path><labID>/<teamID>/
#------------------------------------------------------------------------------
def get_repos(lab, teams):
    for team in teams.keys():
        if teams[team][lab] != None:
            clone_path = "./{}/{}/".format(lab, team)
            if os.path.exists(clone_path):
                shutil.rmtree(clone_path)
            Repo.clone_from(teams[team][lab], "./{}/{}/".format(lab, team))

#------------------------------------------------------------------------------
# lab1 tests when instructor provides no base code
# lab2 tests when instructor does provide base code
# lab3 tests when a student has an empty repo at the deadline
#------------------------------------------------------------------------------
def test():
    teams = parse_teams("./test/teams.json")
    team = teams.keys()[0]
    labs = teams[team].keys()
    for lab in labs:
        get_repos(lab, teams)
        submit_repos(lab, teams["instructor"][lab])
        notify(lab)
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def mossService(lab):
    teams = parse_teams("./teams.json")
    get_repos(lab, teams)
    submit_repos(lab, teams["instructor"][lab])
    notify(lab)

def main(argv):
    if len(argv) > 1:
        if argv[1] == "test":
            test()
        else:
            lab = argv[1]
            mossService(lab)

if __name__ == "__main__":
    main(sys.argv)

