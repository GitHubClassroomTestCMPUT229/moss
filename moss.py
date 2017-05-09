from git import Repo
from mossPython import callScript as mossPy
import sys
import smtplib
import json
# Import the email modules we'll need
from email.mime.text import MIMEText

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

def parse_teams():
    filename = "./teams.json"
    f = open(filename, "r")
    teams = json.load(f)
    return teams
    

# Requirements:
#   Team ids are stored in teams dict
#   Labs are at the next level of the dict
#   Accessing teams[teamID][LabID] return the GitHub url for the team's repo for that lab
# Parameter:
#   lab is used to identify which lab is being pulled
# Effect:
#   Repos are cloned into ./<labID>/<teamID>/
def get_repos(lab):
    teams = parse_teams()
    for team in teams.keys():
        Repo.clone_from(teams[team][lab], "./{}/{}/".format(lab, team))

# Requirements:
#   Must be able to access source code for assignments following structure
#   ./<labID>/<teamID>/
# Parameter:
#   lab is used to identify which lab is being submitted to moss
# Effect:
#   Results of moss comparison are stored in ./<labID>/results.html
#   TODO: GATHER ALL RERFERENCES FROM PAGE THAT IDs SIMILAR SOURCE CODE
def submit_repos(lab):
    mossPy(lab, True)

def main(args):
    lab = args[1]
    get_repos(lab)
    submit_repos(lab)
    notify(lab)

if __name__ == "__main__":
    # main(sys.argv)
    print parse_teams()

