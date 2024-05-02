from openai import OpenAI

class ChatGPTClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)

    def get_completion(self, messages, model="gpt-3.5-turbo-0613"):  
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
        )

        return completion

    def query(self, messages, model="gpt-3.5-turbo-0613"):
        if type(messages) == str:
            messages = [
                {
                    "role": "user",
                    "content": messages,
                },
            ]
        
        completion = self.get_completion(messages, model)
        choices = completion.choices
        msg = choices[0].message

        return msg.content

    def analyze_messages(self, query):
        
        messages = [
            {
                "role": "system",
                "content": "You're an analyzer. Given Slack chats, review the conversations from the past three days. Identify any commitments or tasks that users mentioned they would complete but haven't confirmed completion, and any tasks that others have mentioned they would handle but haven't provided updates on. If you find any, start with 'yes' and give full messages item by item, otherwise, only say 'no'.",
            },
            {
                "role": "user",
                "content": query,
            },
        ]
        
        return self.query(messages)