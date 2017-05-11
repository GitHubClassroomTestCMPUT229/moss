import classroom_manager as cm
import moss
from apscheduler.schedulers.background import BackgroundScheduler

# Trigger collection after deadline
# http://apscheduler.readthedocs.io/en/latest/modules/triggers/date.html

def test():
    print "It's a test!"

def main():
    sched = BackgroundScheduler()
    sched.start()

    job = sched.add_job(test, "interval", seconds=10)

    try:
        org_name = "GitHubClassroomTestCMPUT229"
        hub = cm.login()
        org = cm.get_org(hub, org_name)
        cm.set_teams()
        cm.set_git_teams(hub, org)
        cm.set_repos(org)
        try:
            moss.get_repos("testlab1", cm.get_teams(org))
            # moss.submit_repos("testlab1", cm.get_teams(org)["instructor"]) # To submit with base code
            moss.submit_repos("testlab1", False)    # To submit without base code
        except:
            pass
        moss.clear("testlab1")
    except:
        pass
    cm.del_repos(org)
    cm.del_teams(org)

    job.remove()
    sched.shutdown()

if __name__ == "__main__":
    main()
