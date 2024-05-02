import requests
from datetime import datetime, timedelta

# the output of aggregate_time_entries method is task_id:user_id:time_spent. and this should be changed to task_name:user_name:time_spent
 
class ClickUpClient:
    BASE_URL = "https://api.clickup.com/api/v2"

    def __init__(self, api_key, team_id):
        self.api_key = api_key
        self.team_id = team_id

    def _get_headers(self):
        return {"Authorization": self.api_key}

    def _get_headers_bearer(self):
        return {"Authorization": f"Bearer {self.api_key}"}

    def fetch_users(self):
        url = f"{self.BASE_URL}/team/{self.team_id}/member"
        response = requests.get(url, headers=self._get_headers_bearer())
        if response.status_code == 200:
            users = {member['user']['id']: f"{member['user']['username']}" for member in response.json()['members']}
            return users
        else:
            raise Exception(f"Error fetching users: {response.status_code} {response.text}")

    def fetch_tasks(self):
        url = f"{self.BASE_URL}/team/{self.team_id}/task"
        response = requests.get(url, headers=self._get_headers())
        if response.status_code == 200:
            tasks = {task['id']: task['name'] for task in response.json()['tasks']}
            return tasks
        else:
            raise Exception(f"Error fetching tasks: {response.status_code} {response.text}")

    def _get_yesterday_date(self):
        yesterday = datetime.utcnow() - timedelta(days=1)
        start_of_yesterday = datetime(yesterday.year, yesterday.month, yesterday.day)
        end_of_yesterday = start_of_yesterday + timedelta(days=1) - timedelta(seconds=1)
        return int(start_of_yesterday.timestamp() * 1000), int(
            end_of_yesterday.timestamp() * 1000
        )

    def fetch_time_entries(self):
        start_date, end_date = self._get_yesterday_date()
        url = f"{self.BASE_URL}/team/{self.team_id}/time_entries?start_date={start_date}&end_date={end_date}"
        response = requests.get(url, headers=self._get_headers())
        if response.status_code == 200:
            return response.json()["data"]
        else:
            raise Exception(
                f"Error fetching time entries: {response.status_code} {response.text}"
            )

    def aggregate_time_entries(self, time_entries, users, tasks):
        time_per_task_per_user = {}
        for entry in time_entries:
            user_id = entry["user"]["id"]
            task_id = entry["task"]["id"]
            user_name = users.get(user_id, "Unknown User")
            task_name = tasks.get(task_id, "Unknown Task")
            duration = int(entry["duration"]) / 3600000

            if task_name not in time_per_task_per_user:
                time_per_task_per_user[task_name] = {}
            if user_name not in time_per_task_per_user[task_name]:
                time_per_task_per_user[task_name][user_name] = 0

            time_per_task_per_user[task_name][user_name] += duration

        return time_per_task_per_user

    def aggregate_time_entries(self, time_entries):
        time_per_task_per_user = {}
        for entry in time_entries:
            user_id = entry["user"]["id"]
            task_id = entry["task"]["id"]
            try:
                duration = int(entry["duration"]) / 3600000  
            except ValueError:

                print(f"Error converting duration for task {task_id} and user {user_id}")
                continue  

            if task_id not in time_per_task_per_user:
                time_per_task_per_user[task_id] = {}
            if user_id not in time_per_task_per_user[task_id]:
                time_per_task_per_user[task_id][user_id] = 0

            time_per_task_per_user[task_id][user_id] += duration

        return time_per_task_per_user
    
    def aggregate_time_entries(self):
       
        time_entries = self.fetch_time_entries()
        time_per_task_per_user = {}
        for entry in time_entries:
            user_id = entry["user"]["id"]
            task_id = entry["task"]["id"]
            try:
                duration = int(entry["duration"]) / 3600000  
            except ValueError:

                print(f"Error converting duration for task {task_id} and user {user_id}")
                continue  

            if task_id not in time_per_task_per_user:
                time_per_task_per_user[task_id] = {}
            if user_id not in time_per_task_per_user[task_id]:
                time_per_task_per_user[task_id][user_id] = 0

            time_per_task_per_user[task_id][user_id] += duration

        return time_per_task_per_user
