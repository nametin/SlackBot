This application is a productivity tool that integrates services such as ClickUp, GitHub, Slack, and OpenAI's ChatGPT to analyze and report on project activities. The application fetches data from these services, analyzes it, and generates reports which are sent through Slack.

ChatGptModule.py
Functionality: This module handles interactions with OpenAI's ChatGPT model. It sends queries and processes responses.
Key Methods:
get_completion: Fetches a completion from the GPT model.
query: Sends queries to the GPT model and returns the response.
analyze_messages: Analyzes Slack messages to identify pending commitments or tasks.

ClickUpModule.py
Functionality: Manages interactions with the ClickUp API. It fetches and aggregates task time entries.
Key Methods:
aggregate_time_entries: Aggregates time spent on tasks by different users.
_get_headers: Returns necessary headers for API requests.

GithubModule.py
Functionality: Interfaces with GitHub to retrieve repository activities.
Key Methods:
get_recent_repo_activities_str: Retrieves recent activities from a specified repository.

SlackModule.py
Functionality: Facilitates communication with Slack. It sends messages and gathers chat data.
Key Methods:
send_message_to_ch: Sends messages to specified Slack channels.
get_query: Compiles messages from Slack into a query for analysis.

Main.py
Functionality: Coordinates the operations of all modules. It orchestrates the fetching of data from ClickUp, GitHub, and Slack, and uses the ChatGPT model for analysis.
Flow:
Initialize clients for ClickUp, GitHub, Slack, and ChatGPT.
Gather and send summaries of ClickUp and GitHub data to a Slack channel.
Analyze Slack messages using the ChatGPT module and post the results.
