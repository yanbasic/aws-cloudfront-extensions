import re

import boto3
import sys
from github import Github

# First create a Github instance:

# using an access token
g = Github(sys.argv[0])

# Github Enterprise with custom hostname
# g = Github(base_url="https://github.com/api/v3", login_or_token="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")


print(g.get_user())
# Then play with your Github objects:
for repo in g.get_user().get_repos():
    if repo.name == 'aws-cloudfront-extensions':
        print(repo.url)
        for pull in repo.get_pulls():
            print(pull.title)
            pull.create_issue_comment('test comments')
            pull.add_to_labels('test label 2')


# Add CI-Succeed label to the PR
def ci_success(repo_name, pull_id):
    g.get_user().get_repo(repo_name).get_pull(pull_id).add_to_labels('CI-Succeed')
