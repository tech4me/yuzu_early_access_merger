import sys
from datetime import datetime
from github import Github
from git import Repo

yuzu_dir = ""
login_token = ""
early_access = True

repo = Repo(yuzu_dir)

def merge_pr(pr_num):
    repo.git.fetch("origin", "pull/{PR}/head".format(PR=pr_num))
    repo.git.merge("--no-edit", "FETCH_HEAD")

if repo.is_dirty():
    print("Abort! yuzu repo is dirty")
    sys.exit()
repo.git.checkout("master")
repo.git.pull("origin", "master")
repo.git.branch(D="new_branch")
repo.git.checkout(b="new_branch")

g = Github(login_token)
print("GitHub rate remaining:", g.rate_limiting[0])
print("GitHub rate limit:", g.rate_limiting[1])
print("GitHub rate reset time:", datetime.fromtimestamp(g.rate_limiting_resettime).strftime('%Y-%m-%d %H:%M:%S'))
yuzu_repo = g.get_repo("yuzu-emu/yuzu")
print("Using url: " + yuzu_repo.url)
for pull in yuzu_repo.get_pulls():
    for label in pull.get_labels():
        if label.name == "mainline-merge":
            print("Merging mainline PR:", pull.number, "Title:", pull.title)
            merge_pr(pull.number)
        elif early_access and label.name == "early-access-merge":
            print("Merging early access PR:", pull.number, "Title:", pull.title)
            merge_pr(pull.number)