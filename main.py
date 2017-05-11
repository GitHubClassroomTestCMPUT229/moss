from classroom_manager import Manager
import moss
import json
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

# Trigger collection after deadline
# http://apscheduler.readthedocs.io/en/latest/modules/triggers/date.html

def rel():
    print "RELEASE SIMULATION "
def col():
    print "COLLECTION SIMULATION "

def main():
    try:
        org_name = "GitHubClassroomTestCMPUT229"
        m = Manager(org_name)
        m.set_teams()
        m.set_git_teams()
        m.set_repos("testlab1")
        try:
            moss.get_repos("testlab1", cm.get_teams(org))
            # moss.submit_repos("testlab1", cm.get_teams(org)["instructor"]) # To submit with base code
            moss.submit_repos("testlab1", False)    # To submit without base code
        except:
            pass
        moss.clear("testlab1")
    except:
        pass
    m.del_repos()
    m.del_teams()

    job.remove()
    sched.shutdown()

if __name__ == "__main__":
    f = open("./class/deadlines.json", "r")
    deadlines = json.load(f)
    sched = BackgroundScheduler()
    sched.start()
    jobs = []

    for lab in deadlines:
        for t in deadlines[lab]:
            if t == "release":
                job = sched.add_job(rel, "date", run_date=deadlines[lab][t])
                jobs.append(job)
            elif t == "collect":
                job = sched.add_job(col, "date", run_date=deadlines[lab][t])
                jobs.append(job)


    #job = sched.add_job(main, "date", run_date=datetime(2017, 5, 11, 14, 11))

