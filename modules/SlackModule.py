import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime, timedelta
import logging


class SlackClient:
    def __init__(self, token):
        self.client = WebClient(token=token)
        self.channels_list = []

    def get_user_name(self, user_id):
        try:
            response = self.client.users_info(user=user_id)
            if response["ok"]:
                try:
                    user_name = response["user"]["real_name"]  
                except:
                    user_name = response["user"]["name"]
                return user_name
            else:
                logging.error(
                    f"Failed to fetch user name for ID {user_id}: {response['error']}"
                )
                return None
        except SlackApiError as e:
            logging.error(
                f"Error fetching user name for ID {user_id}: {e.response['error']}"
            )
            return None

    def fetch_channels(self):
        """Fetches all channels where the bot is a member."""
        try:
            response = self.client.conversations_list(
                types="public_channel,private_channel"
            )
            channels = response["channels"]
            for channel in channels:
                self.channels_list.append(channel)
        except SlackApiError as e:
            logging.error(f"Error fetching channels: {e}")

    def _join_channel(self, channel_id):
        """Attempts to add the bot to the specified channel."""
        try:
            response = self.client.conversations_join(channel=channel_id)
            if response["ok"]:
                return True
            else:
                return False
        except SlackApiError as e:
            logging.error(f"Error joining channel {channel_id}: {e.response['error']}")
            return False

    # if bot isn't joined a public channel, then it joins itself.
    # But private channel joins should be done manually
    def fetch_messages(self, days=3):
        self.fetch_channels()
        """Fetch messages from all channels over the last three days."""
        messages = []
        current_time = datetime.now()
        oldest_time = (current_time - timedelta(days=days)).timestamp()

        for channel in self.channels_list:
            channel_id = channel["id"]
            try:
                response = self.client.conversations_history(
                    channel=channel_id, oldest=str(oldest_time)
                )
                messages.extend(response["messages"])
            except SlackApiError as e:
                if e.response["error"] == "not_in_channel":
                    if self._join_channel(channel_id):
                        response = self.client.conversations_history(
                            channel=channel_id, oldest=str(oldest_time)
                        )
                        messages.extend(response["messages"])
                else:
                    logging.error(f"Error fetching messages from {channel_id}: {e}")

        return messages

    def find_channel_id(self, channel_name):
        try:
            self.fetch_channels()

            for channel in self.channels_list:
                if channel["name"] == channel_name:
                    return channel["id"]

        except SlackApiError as e:
            logging.error(f"Error fetching channels: {e}")

    def send_message_to_ch(self, ch, message):

        if not ch.isnumeric():
            ch = self.find_channel_id(ch)

        try:
            response = self.client.chat_postMessage(
                channel = ch, 
                text = message
            )
            if response["ok"]:
                return True
            else:
                return False
        except SlackApiError as e:
            print(e)

    def get_query(self):
        messages = self.fetch_messages()
        query =""
        for message in messages:
            text = message['text']
            if (not "joined" in text) and not "@U070U2WCK7G" in text:
                msg = f"{self.get_user_name(message['user'])}: {text}\n"
                query+=msg
        return query
