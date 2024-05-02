import requests
from datetime import datetime


class GitHubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self, token, owner):
        self.token = token
        self.owner = owner

    def _get_headers(self):
        return {"Authorization": f"token {self.token}"}

    def _get_yesterday_date(self):
        # yesterday = datetime.utcnow().date() - timedelta(days=1)
        yesterday = datetime.utcnow().date()

        return yesterday.isoformat()

    def get_user_repos(self):
        """
        Fetch all repositories for the authenticated user, including private repositories.
        """
        url = f"{self.BASE_URL}/user/repos"  
        response = requests.get(url, headers=self._get_headers())
        if response.status_code == 200:
            return [repo['name'] for repo in response.json() if repo['owner']['login'] == self.owner]
        else:
            raise Exception(f"Error fetching repositories: {response.status_code} {response.text}")

    def get_repo_activity(self, repo):
        """
        Fetch detailed commit activity for the given repository, including additions and deletions.
        """
        if repo != "SlackBot":
            return []

        date = self._get_yesterday_date()
        commits_url = f"{self.BASE_URL}/repos/{self.owner}/{repo}/commits?since={date}T00:00:00Z&until={date}T23:59:59Z"
        response = requests.get(commits_url, headers=self._get_headers())
        if response.status_code == 200:
            commit_data = []
            commits = response.json()
            for commit_parent in commits:

                # to get additions and deletions, send one more request to get commit detail
                commit_detail_url = commit_parent["url"]  
                commit= commit_parent["commit"]
                commit_response = requests.get(commit_detail_url, headers=self._get_headers())

                if commit_response.status_code == 200:
                    commit_detail = commit_response.json()

                    if "stats" in commit_detail:
                        stats = commit_detail["stats"]
                        commit_data.append(
                            {
                                "committer": commit["committer"]["name"],
                                "commit_date": commit["committer"]["date"],
                                "commit_message": commit["message"],
                                "project_name": repo,
                                "added_lines": stats["additions"],
                                "changed_lines": stats["deletions"],
                            }
                        )
                    else:
                        commit_data.append(
                            {
                                "committer": commit["committer"]["name"],
                                "commit_date": commit["committer"]["date"],
                                "commit_message": commit["message"],
                                "project_name": repo,
                                "added_lines": stats["additions"],
                                "changed_lines": stats["deletions"],
                                "note": "No change data available",
                            }
                        )

            return commit_data
        else:
            raise Exception(f"Error fetching GitHub commits: {response.status_code} {response.text}")

    def get_recent_repo_activities(self):
        repos = self.get_user_repos()
        
        activities = []
        
        for repo in repos:
            github_data = self.get_repo_activity(repo)
            if len(github_data) == 0:
                continue
            for data in github_data:
                activities.append(data)
                # print(data)

        return activities

    def get_recent_repo_activities_str(self):
        activities = self.get_recent_repo_activities()
        return "\n".join(
            [
                f"{activity['committer']} committed to {activity['project_name']} with {activity['added_lines']} additions and {activity['changed_lines']} deletions: {activity['commit_message']}"
                for activity in activities
            ]
        )