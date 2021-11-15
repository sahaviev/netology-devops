#!/usr/bin/env python3

from github import Github
import os
import sys
import subprocess
import calendar
import time

ACCESS_TOKEN = ''
REPO_NAME = 'python-test'
MASTER_BRANCH = 'master'

g = Github(ACCESS_TOKEN)

timestamp = calendar.timegm(time.gmtime())

if len(sys.argv) > 1 and not os.path.isdir(sys.argv[1]):
    sys.exit('project not founded, check directory path: ' + sys.argv[1])

project_folder = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
print('project_folder: ' + project_folder)


def git_status():
    proc = subprocess.run(['git', 'status'], cwd=project_folder)
    for result in str(proc.stdout).split('\\n'):
        print(result)


def git_create_branch(_branch_name):
    subprocess.run(['git', 'checkout', '-b', _branch_name], cwd=project_folder)


def git_commit(message):
    subprocess.run(['git', 'commit', '-am', message], cwd=project_folder)


def git_push(_branch_name):
    subprocess.run(['git', 'push', '--set-upstream', 'origin', _branch_name], cwd=project_folder)


def github_create_pull_request(_branch_name, _title, _body):
    repo = g.get_user().get_repo(REPO_NAME)
    repo.create_pull(title=_title, body=_body, head=_branch_name, base=MASTER_BRANCH)


git_status()
new_branch_name = 'config/' + str(timestamp)
git_create_branch(new_branch_name)
commit_message = 'CONFIG: update configuration. v' + str(timestamp)
git_commit(commit_message)
git_push(new_branch_name)

title = "AUTO-UPDATE: update configuration to version " + str(timestamp)

if sys.argv[2]:
    body = sys.argv[2]
else:
    body = 'Update configuration to version'

github_create_pull_request(new_branch_name, title, body)
