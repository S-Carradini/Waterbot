from get_completion_from_message import GetCompletionFromMessages
from datetime import datetime
# To check user's intent 
def UserIntentCheck (user_query):
    print('timestamp entering user intent check: ',datetime.now().strftime('%H:%M:%S'))
    user_intent_check_message =  [
{'role':'system',
 'content': "Please review the following user query and assess if the user has bad intentions of harm to self or others, harassment, or violence. \
    If the user has bad intentions, ouput boolean 'True', else ouput boolean 'False'. "},
{'role':'user',
 'content':user_query},
]
    user_intent_response = GetCompletionFromMessages(user_intent_check_message, temperature=0.0)
    string_to_boolean = {"true": True, "false": False}
    user_intent = string_to_boolean.get(user_intent_response.lower())
    print('timestamp after user intent check: ',datetime.now().strftime(' %H:%M:%S'))
    return user_intent

