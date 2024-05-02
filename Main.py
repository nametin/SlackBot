from modules.ClickUpModule import ClickUpClient
from modules.GithubModule import GitHubClient
from modules.ChatGptModule import ChatGPTClient
from  modules.SlackModule import SlackClient

def main():
    clickup_api_key = "clickup_api_key"
    clickup_team_id = "clickup_team_id"

    github_token = "github_token"
    repo_owner = "repo_owner"

    chatgpt_api_key = "chatgpt_api_key"

    slack_bot_user_auth_token = "slack_bot_user_auth_token"
    
    clickup_client = ClickUpClient(clickup_api_key, clickup_team_id)
    github_client = GitHubClient(github_token, repo_owner)
    chatgpt_client = ChatGPTClient(chatgpt_api_key)
    slack_client = SlackClient(slack_bot_user_auth_token)

    try:

        clickup_data = clickup_client.aggregate_time_entries()
        
        slack_client.send_message_to_ch("ch_that_only_bot_talks","A summary of clickup data is as follows:")
        slack_client.send_message_to_ch("ch_that_only_bot_talks",clickup_data)

        github_data = github_client.get_recent_repo_activities_str()
        slack_client.send_message_to_ch("ch_that_only_bot_talks","A summary of github data is as follows:")
        slack_client.send_message_to_ch("ch_that_only_bot_talks",github_data)

        query = slack_client.get_query()
        answer = chatgpt_client.analyze_messages(query)

        slack_client.send_message_to_ch("ch_that_only_bot_talks","The analysis of the slack messages is as follows:")
        if answer.startswith("yes") or answer.startswith("Yes"):
            slack_client.send_message_to_ch("ch_that_only_bot_talks", answer)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
