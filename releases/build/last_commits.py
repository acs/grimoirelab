#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Get the last commits for GrmoireLab repositories
#
# Copyright (C) 2017 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors:
#   Alvaro del Castillo San Felix <acs@bitergia.com>
#

import argparse

import requests

ORG = 'chaoss'
GITHUB_REPOS_API = 'https://api.github.com/repos' + '/' + ORG
GITHUB_ORGS_API = 'https://api.github.com/orgs' + '/'+ ORG

def get_params():
    parser = argparse.ArgumentParser(usage="usage:last_commits.py [options]",
                                     description="Collect the last commit " + \
                                                  "from GrimoireLab repositories")
    parser.add_argument("-t", "--token", required=True, help="GitHub API token")

    return parser.parse_args()

def send_github(url, headers=None):
    headers = {'Authorization': 'token ' + args.token }
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res

def get_repositories():
    repos_url = GITHUB_ORGS_API + "/repos"
    page = 1

    while True:
        res = send_github(repos_url + "?page=%i" % page)
        page += 1  # Prepara for next page request
        res.raise_for_status()

        repos_dict = res.json()

        if not repos_dict:
            break

        for repo in repos_dict:
            if "grimoirelab" not in repo['name']:
                continue
            yield repo['name']

if __name__ == '__main__':

    args = get_params()

    for repo in get_repositories():
        # Return the last commit from master branch
        commits_url = GITHUB_REPOS_API + "/" + repo + "/commits/master"
        res = send_github(commits_url)
        commit = res.json()['sha']
        repo_name = repo.upper().replace("GRIMOIRELAB-", "").replace("-", "_").replace(".", "_")
        # Some exceptions to teh general rules
        if repo_name == "TOOLKIT":
            repo_name = "GRIMOIRELAB_TOOLKIT"
        elif repo_name == "ELK":
            repo_name = "GRIMOIREELK"
        elif repo_name == "SIRMORDRED":
            repo_name = "MORDRED"
        print(repo_name + "='" + commit + "'")
