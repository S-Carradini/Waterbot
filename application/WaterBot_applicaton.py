# Importing necessary modules and packages
from werkzeug.datastructures import ImmutableMultiDict
from flask import Flask, render_template, request,  send_from_directory, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from get_completion_from_message import GetCompletionFromMessages
from moderation_check import ModerationCheck
from user_intent_check import UserIntentCheck
from prompt_injection_check import PromptInjectionCheck
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import re
import openai
import os
import threading
from threading import Thread
from uuid import uuid4
from openai import OpenAI
from chatbot_memory import ChatbotMemory
from source_metadata import LookupWebsource

# Initializing Flask app
app = Flask(__name__, template_folder='templates')
app.secret_key = 'asdfghjkl1234567890'
app.config['SESSION_TYPE'] = 'filesystem'
api_key_file_path = 'openai_api_key.txt'
#os.environ['DATABASE_URL'] = "postgres://zmsatwzykkntar:51d4a604128d4424a8e5d0f206d16c418ad99c5db56bca9021891da202b618e5@ec2-52-73-166-232.compute-1.amazonaws.com:5432/d73l0t540al4dn"

# Reading the OpenAI API key from a file
with open(api_key_file_path, 'r') as file:
    api_key = file.read().strip()

# Setting the API key for OpenAI
os.environ['OPENAI_API_KEY'] = api_key


from openai import OpenAI
client = OpenAI()
memory = ChatbotMemory()
message_count = dict()

# Initializing embeddings and vector store
embeddings = OpenAIEmbeddings()
vectordb = Chroma(persist_directory="docs_new/chroma/", embedding_function=embeddings)

# Route to serve static files from templates folder
@app.route('/templates/<path:path>')
def send_style(path):
    return send_from_directory('templates', path)

# Route to serve images
@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('templates/images', path)

# Route to serve styles.css file
@app.route('/styles.css')
def send_style_css():
    return send_from_directory('templates', 'styles.css')

# Route to serve utils.js file
@app.route('/utils.js')
def send_js():
    return send_from_directory('templates', 'utils.js')

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle submission of ratings
@app.route('/submit_rating_api', methods=['POST'])
def submit_rating():
    data_to_sql = {}
    for key, value in request.form.items():
        data_to_sql[key] = value
    memory.SaveRatings(data_to_sql)
    return "Done"

#####################################################################################################################
# Route to handle chat interactions
@app.route('/chat_api', methods=['POST'])
def chat_api():
    if 'uuid' not in session:
        session['uuid'] = uuid4()
        message_count[session['uuid']] = 0

    if session['uuid'] not in message_count:
        message_count[session['uuid']] = 0
    user_query = request.form['user_query']
    user_message = {"role":"user","content":user_query}

    check_results = [] # to store results from moderation and user intent checks

# Create two threads
    thread1 = threading.Thread(target=lambda: check_results.append(ModerationCheck(user_query)))
    thread2 = threading.Thread(target=lambda: check_results.append(UserIntentCheck(user_query)))

# Start the threads
    thread1.start()
    thread2.start()

# Wait for both threads to finish
    thread1.join()
    thread2.join()

    print("Both threads have finished.")
    ModerationCheck_result = check_results[0]
    UserIntentCheck_result = check_results[1]

    if ModerationCheck_result or UserIntentCheck_result:
        response = 'I am sorry, your request is inappropriate and I cannot answer it.'
        msgID = memory.add_message_to_session(session['uuid'],user_query, response)
        return jsonify({"resp":response, "msgID": msgID})
    if PromptInjectionCheck(user_query):
        response = 'I am sorry, your request cannot be handled.'
        msgID = memory.add_message_to_session(session['uuid'],user_query, response)
        return jsonify({"resp":response, "msgID": msgID})
   
    docs = vectordb.similarity_search(user_query)
    print('docs\n', docs)
    sources = []
    qdocs1 = []

    for i in range(len(docs)):
        sources = [str(docs[i].metadata['source'])]
        qdocs1 = [" ".join(docs[i].page_content)]
    source_list = []
    for source in sources:
        # match = re.search(r'/(\d{4}\s.*?)$', source) or re.search(r'/(\d{4}\s.*?)$', source)
        match = os.path.basename(source)
        if match:
            websource = LookupWebsource(match)
            source_list.append(websource)
    system_message = {"role":"system", "content": f"You are a helpful assistant named Blue that provides information about water in Arizona.\
You will be provided with Arizona water related queries. Answer the queries briefly in 3 to 4 sentences.\
The governor of Arizona is Katie Hobbs.\
When asked the name of the governor or current governor you should respond with the name Katie Hobbs.\
For any other inquiries regarding the names of elected officials excluding the name of the governor, you should respond: 'The most current information on the names of elected officials is available at az.gov.'\
Verify not to include any information that is irrelevant to the current query. Use the following information to \
answer the queries in a friendly tone {qdocs1}"}
    messages = [system_message]

    history = memory.get_history(session['uuid'])
    for message in history:
        messages.append(message)
    messages.append(user_message)
    
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.5,
        stream=False  # we set stream=True
    )
    bot_response = response.choices[0].message.content
    
    if source_list:
        msgID = memory.add_message_to_session(session['uuid'],user_query, bot_response, source_list)
    else:
        msgID = memory.add_message_to_session(session['uuid'],user_query, bot_response)
    bot_response = re.sub(r'\n', '<br>', bot_response)
    # Define a regular expression pattern to find text between ** and **
    pattern = r"\*\*(.*?)\*\*"
    bot_response = re.sub(pattern, r"<strong>\1</strong>", bot_response)
    
    return jsonify({"resp":bot_response, "msgID": msgID})

#####################################################################################################################
@app.route('/chat_description_api', methods=['POST'])
def chat_descripiton():
    previous_query_response = memory.get_messages_for_session(session['uuid'])
    user_query = previous_query_response[0]['content']
    previous_response = previous_query_response[1]['content']
    search_query = user_query+previous_response
    docs = vectordb.similarity_search(search_query)
    sources = []
    qdocs1 = []
    # docs = vectordb.similarity_search(user_query)
    for i in range(len(docs)):
        sources = [str(docs[i].metadata['source'])]
        qdocs1 = [" ".join(docs[i].page_content)]
    source_list = []
    for source in sources:
        match = re.search(r'/(\d{4}\s.*?)$', source) or re.search(r'/(\d{4}\s.*?)$', source)
        if match:
            websource = LookupWebsource(match.group(1))
            source_list.append(websource)

    system_message = {"role":"system", "content":f"Take a breath and provide a longer answer to the previous question, providing \
                      more explanation and reasoning. Use the following information to \
                        answer in a friendly tone {docs}"}
    messages = [system_message]
    messages.append(previous_query_response[0])
    messages.append(previous_query_response[1])
    # history = memory.get_messages_for_session(session['uuid'])[0]['content']
    
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.5,
        stream=False  # we set stream=True
    )
    bot_response = response.choices[0].message.content
    
    if source_list:
        msgID = memory.add_message_to_session(session['uuid'],user_query, bot_response, source_list)
    else:
        msgID = memory.add_message_to_session(session['uuid'],user_query, bot_response)
    bot_response = re.sub(r'\n', '<br>', bot_response)
    # Define a regular expression pattern to find text between ** and **
    pattern = r"\*\*(.*?)\*\*"
    bot_response = re.sub(pattern, r"<strong>\1</strong>", bot_response)
    return jsonify({"resp":bot_response, "msgID": msgID})

#####################################################################################################################
@app.route('/chat_short_api', methods=['POST'])
def chat_short():
    system_message = {"role":"system", "content":"Summarize the previous answer in two sentences."}
    messages = [system_message]
    previous_query_response = memory.get_messages_for_session(session['uuid'])
    user_query = previous_query_response[0]['content']
    previous_response = previous_query_response[1]['content']
    messages.append(previous_query_response[0])
    messages.append(previous_query_response[1])
    # history = memory.get_messages_for_session(session['uuid'])[0]['content']
    
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.5,
        stream=False  # we set stream=True
    )
    bot_response = response.choices[0].message.content
    msgID = memory.add_message_to_session(session['uuid'],user_query, bot_response)
    bot_response = re.sub(r'\n', '<br>', bot_response)
    # Define a regular expression pattern to find text between ** and **
    pattern = r"\*\*(.*?)\*\*"
    bot_response = re.sub(pattern, r"<strong>\1</strong>", bot_response)
    return jsonify({"resp":bot_response, "msgID": msgID})

#####################################################################################################################
@app.route('/chat_detailed_api', methods=['POST'])
def chat_detailed():
    previous_query_response = memory.get_messages_for_session(session['uuid'])
    user_query = previous_query_response[0]['content']
    previous_response = previous_query_response[1]['content']
    search_query = user_query+previous_response
    docs = vectordb.similarity_search(search_query)
    sources = []
    qdocs1 = []
    for i in range(len(docs)):
        sources = [str(docs[i].metadata['source'])]
        qdocs1 = [" ".join(docs[i].page_content)]
    source_list = []
    for source in sources:
        match = re.search(r'/(\d{4}\s.*?)$', source) or re.search(r'/(\d{4}\s.*?)$', source)
        if match:
            websource = LookupWebsource(match.group(1))
            source_list.append(websource)

    system_message = {"role":"system", "content":f"Take a breath and provide a more detailed answer to the previous question\
                      providing more explanation and reasoning, using statistics, \
                      examples, and proper nouns. Use the following information to \
                        answer in a friendly tone {docs}"}
    messages = [system_message]
    messages.append(previous_query_response[0])
    messages.append(previous_query_response[1])
    # history = memory.get_messages_for_session(session['uuid'])[0]['content']
    
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.5,
        stream=False  # we set stream=True
    )
    bot_response = response.choices[0].message.content
    
    if source_list:
        msgID = memory.add_message_to_session(session['uuid'],user_query, bot_response, source_list)
    else:
        msgID = memory.add_message_to_session(session['uuid'],user_query, bot_response)
    bot_response = re.sub(r'\n', '<br>', bot_response)
    # Define a regular expression pattern to find text between ** and **
    pattern = r"\*\*(.*?)\*\*"
    bot_response = re.sub(pattern, r"<strong>\1</strong>", bot_response)
    return jsonify({"resp":bot_response, "msgID": msgID})

#####################################################################################################################
@app.route('/chat_actionItems_api', methods=['POST'])
def chat_actionItems():
    previous_query_response = memory.get_messages_for_session(session['uuid'])
    user_query = previous_query_response[0]['content']
    previous_response = previous_query_response[1]['content']
    search_query = user_query+previous_response
    docs = vectordb.similarity_search(search_query)
    sources = []
    qdocs1 = []
    for i in range(len(docs)):
        sources = [str(docs[i].metadata['source'])]
        qdocs1 = [" ".join(docs[i].page_content)]
    source_list = []
    for source in sources:
        match = re.search(r'/(\d{4}\s.*?)$', source) or re.search(r'/(\d{4}\s.*?)$', source)
        if match:
            websource = LookupWebsource(match.group(1))
            source_list.append(websource)

    system_message = {"role":"system", "content":f"Provide three action items that the user can implement in relation to the previous question, \
                      explaining each step by step. Use the following information to \
                        answer in a friendly tone {docs}"}
    messages = [system_message]
    messages.append(previous_query_response[0])
    messages.append(previous_query_response[1])
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.5,
        stream=False  # we set stream=True for streaming response
    )
    bot_response = response.choices[0].message.content
    if source_list:
        msgID = memory.add_message_to_session(session['uuid'],user_query, bot_response, source_list)
    else:
        msgID = memory.add_message_to_session(session['uuid'],user_query, bot_response)
    bot_response = re.sub(r'\n', '<br>', bot_response)

    # Define a regular expression pattern to find text between ** and **
    pattern = r"\*\*(.*?)\*\*"
    bot_response = re.sub(pattern, r"<strong>\1</strong>", bot_response)
    return jsonify({"resp":bot_response, "msgID": msgID})

#####################################################################################################################
@app.route('/chat_sources_api', methods=['POST'])
def chat_sources():
    previous_query_response = memory.get_sources(session['uuid'])
    source = previous_query_response[2]
    user_query = previous_query_response[0]['content']
    previous_response = previous_query_response[1]['content']
    system_message = {"role":"system", "content":f"Report sources used in the previous answer with the links to their webpage \
                      from the following sources: {source}."}
    messages = [system_message]
    messages.append(previous_query_response[0])
    messages.append(previous_query_response[1])
    
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.5,
        stream=False  # we set stream=True
    )
    bot_response = response.choices[0].message.content
    msgID = memory.add_message_to_session(session['uuid'],user_query, bot_response)

    bot_response = re.sub(r'\n', '<br>', bot_response)
    # Define a regular expression pattern to find text between ** and **
    pattern = r"\*\*(.*?)\*\*"
    bot_response = re.sub(pattern, r"<strong>\1</strong>", bot_response)
    return jsonify({"resp":bot_response, "msgID": msgID})
    
# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)
