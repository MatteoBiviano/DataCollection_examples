#pip install PyGithub
"""
***** Examples of results that can be obtained *****
- Search for repositories of a specific user ("ex: mojombo")
 	https://api.github.com/users/mojombo/repos

- Search for contributors of a specific repository of a specific user ("ex: mojombo/chronic")
	https://api.github.com/repos/mojombo/chronic/contributors

- Search for followers of a specific user
	https://api.github.com/users/mojombo/followers

- Search for starred of a specific user
	https://api.github.com/users/mojombo/starred
"""


from github import Github
import json
from collections import *
import networkx as nx
import re
import csv
import time
import os
import pandas as pd
from pandas import DataFrame


# Github API access token
ACCESS_TOKEN = ""

g = Github(ACCESS_TOKEN)

"""
1) Search for a specific list of keywords, by selecting:
- repo name (user/reponame)
- user name 
- language
- #star 
- #forks
"""
programming_keywords = ["python", "php", "java", "c#", "f#", "javascript"]

repo_name = []
repo_owner = []
repo_language = []
repo_stargazers_count = []
repo_forks = []
for language in programming_keywords:
    print(f"**** Language {language} ****")
    repositories = g.search_repositories(query='language:'+str(language))
    it = 0
    for repo in repositories:
        print(f"Iteration: {it}")
        repo_name.append(repo.full_name)
        repo_owner.append(repo.owner.login)
        repo_stargazers_count.append(repo.stargazers_count)
        repo_language.append(repo.language)
        repo_forks.append(repo.forks_count)
        it = it + 1
        if it == 3000: #Max 3k repo for user
            break
        if it%200 == 0: #Max 200 it every 10 secs
            time.sleep(10)
#Saving
df = pd.DataFrame({'Name': repo_name, 'Owner': repo_owner, 'Language': repo_language, 'Stars': repo_stargazers_count, 'Forks': repo_forks})
print(df)
df.to_csv("Dataset/repositories.csv", index=False)


"""
2) Get the stargazers for repositories

"""
dt = {}
for repo in repo_name:
    print(f"****** Repository: {repo} ****")
    stargazers = []
    it = 0
    repo = g.get_repo(repo)
    for user in repo.get_stargazers():
        stargazers.append(user)
        it = it + 1
        if it%200 == 0:
            time.sleep(10)
        print(f"Iteration: {it}")
    dt[repo] = stargazers