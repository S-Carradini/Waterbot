from openai import OpenAI
from datetime import datetime

def ModerationCheck(user_query):
    print('timestamp starting moderation check: ',datetime.now().strftime(' %H:%M:%S'))
    client = OpenAI()
    response = client.moderations.create(input=user_query)
    moderation_output = response.results[0].flagged
    print('timestamp exiting moderation check: ',datetime.now().strftime(' %H:%M:%S'))
    return moderation_output


