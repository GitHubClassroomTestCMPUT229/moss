import classroom_manager as cm
import moss

def main():
    try:
        org_name = "GitHubClassroomTestCMPUT229"
        hub = cm.login()
        org = cm.get_org(hub, org_name)
        cm.set_teams()
        cm.set_git_teams(hub, org)
        cm.set_repos(org)
        moss.get_repos("testlab1", cm.get_teams(org))
        # moss.submit_repos("testlab1", cm.get_teams(org)["instructor"]) # To submit with base code
        moss.submit_repos("testlab1", False)    # To submit without base code
    except:
        pass
    cm.del_repos(org)
    cm.del_teams(org)

if __name__ == "__main__":
    main()
