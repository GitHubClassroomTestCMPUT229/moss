from classroom_manager import Manager
import moss
import json
# from apscheduler.schedulers.background import BackgroundScheduler
# from datetime import datetime

# Trigger collection after deadline
# http://apscheduler.readthedocs.io/en/latest/modules/triggers/date.html

def main():
    try:
        org_name = "GitHubClassroomTestCMPUT229"
        m = Manager(org_name)
        print "Setting teams locally."
        m.set_teams()   
        raw_input("Teams parsed.  Press [enter] to continue.")
        m.set_git_teams()
        raw_input("Teams added to organization.  Press [enter] to continue.")
        m.set_repos("testlab1")
        raw_input("Repos distributed to teams.  Press [enter] to continue.")
        
        try:
            moss.get_repos("testlab1", m.get_teams())
            raw_input("Repos gathered for moss. Press [enter] to continue.")
            # moss.submit_repos("testlab1", cm.get_teams(org)["instructor"]) # To submit with base code
            moss.submit_repos("testlab1", False)    # To submit without base code
            moss.copy_response("testlab1")
            raw_input("Repos submitted to moss.  Press [enter] to continue.")
        except Exception as e:
            print "Error with moss"
            print e
        print "Sending notification."
        moss.notify("testlab1")
        moss.clear("testlab1")
        raw_input("Moss files cleared.  Press [enter] to continue.")
    except:
        pass
    m.del_repos()
    raw_input("Press [enter] to continue.")
    m.del_teams()
    raw_input("Press [enter] to continue.")

if __name__ == "__main__":
    main()


