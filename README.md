# Waterbot

The public home of Arizona Water Innovation Initiative's Waterbot project

## Overview

The Arizona Water Chatbot, developed by an interdisciplinary research team, is designed to deliver accurate and user-friendly information about Arizona's water situation to residents. This OpenAI-powered chatbot uses a retrieval-augmented generation approach to provide context-sensitive and relevant responses, incorporating guardrails to mitigate malicious content. It is distinct in its ability to represent Indigenous perspectives on water, providing a holistic view of water's role in Arizona, including perspectives from the 23 Indigenous nations within the state.

## Architecture

The architecture includes four main stages: ingestion, retrieval, synthesis, and output evaluation, with an intricate process to maintain data integrity and context.

### Ingestion Phase 

This phase is crucial for creating a rich knowledge base for the chatbot. Documents related to Arizona's water resources are broken down into manageable chunks, which are then converted into embeddings. The process of creating embeddings allows the user to convert textual data into numerical strings organized in a vector database that enables efficient retrieval of contextually relevant information.

A meticulous chunking process with a 10% overlap ensures contextual integrity within these chunks. These embeddings form the foundation of the chatbot's response capability.

These processes of Data Chunking and Overlap ensure preservation of context when segmenting documents, crucial for maintaining the integrity of the information.

### Retrieval Phase

When a query is received, the chatbot performs several security checks to ensure the integrity and safety of the responses. These safety checks include moderation, prompt injection, and user intent checks to ensure responses align with ethical guidelines and user safety.

1. Moderation Check: Filters out content that may violate usage policies using OpenAI’s Moderation API.

2. Prompt Injection Check: Prevents the bot from being misled by malicious or irrelevant prompts.

3. User Intent Check: Assesses potential harm in the user's query.

Following these checks, the query is embedded and matched against the knowledge base to identify relevant information.

After the checks, we employ cosine similarity search to match the user's query with the most relevant information based on cosine similarity metrics.

### Synthesis Phase 

This stage involves creating a composite input from the query embeddings, possible response embeddings, and additional context. The GPT-3.5 Turbo model processes this composite input, leveraging its pre-trained capabilities to generate a coherent and contextually relevant response. This generation process aims for responses that are informed by the user's query and the conversation history.

Recognizing the importance of representing Indigenous perspectives on water, the chatbot was trained on a mix of municipal and Indigenous sources. This ensures that responses reflect the diverse viewpoints and historical contexts relevant to Arizona's water resources, especially when addressing common questions related to water supply and demands. Information from these perspectives are included in the vector embeddings that are part of the generation process.

### Output Evaluation Phase

The generated response is evaluated against a set of criteria including accuracy, relevance to the query, and groundedness in the conversation's context. This evaluation is part of an iterative process that incorporates user feedback to continuously improve the chatbot's performance.
 
## Methods

To develop a chatbot using Chat GPT 3.5-Turbo's API, the following procedures need to be followed:

### Data Collection

The first step is to collect data related to the topic the chatbot will be designed for. In the case of developing a chatbot to answer all questions about water in the state of Arizona, data collection should focus on gathering information on water sources, water usage patterns, conservation measures, and other related topics. The data should be in the form of questions and answers related to the topic.

### Data Preprocessing

Once the data is collected, it needs to be pre-processed to remove any irrelevant information and reformat it into a usable form. This includes removing stop words, stemming, and tokenization. Preprocessing can be done using tools like Python and Natural Language Toolkit (NLTK).

### Model Training

The pre-processed data is then used to train the machine learning model. The machine learning models used in Chat GPT 3.5's API are highly sophisticated and require extensive training to perform accurately. The more data the model is trained on, the more accurate it becomes.

### Model Testing

After the model is trained, it needs to be tested to ensure that it is providing accurate responses to user queries. Testing involves providing the model with a set of questions and evaluating its responses. The testing process should include both automated and manual testing to ensure that the chatbot is accurately responding to user queries.

### Integration

Once the model is tested and proven to be accurate, it can be integrated into a chatbot platform. The chatbot platform should be designed to handle user queries related to water in Arizona and provide accurate responses based on the machine learning model. The chatbot platform can be developed using a variety of programming languages like Python, Ruby, or Node.js.

### Recommendations

The following steps are recommended to ensure that the chatbot is effective and accurate:   

1. Collect data related to water in Arizona, including questions and answers related to the topic. This data can be collected from a variety of sources, including government websites, water conservation organizations, and news articles.
   
2. Pre-process the data to remove any irrelevant information and reformat it into a usable form. This can be done using tools like Python and NLTK. Preprocessing should include removing stop words, stemming, and tokenization.
   
3. Train the machine learning model using the pre-processed data. Use Chat GPT 3.5's API to train the model and ensure that it can understand the context of the questions and provide accurate responses. The model should be trained on a large dataset to ensure that it can answer a wide range of questions related to water in Arizona.

4. Test the model by providing it with a set of questions related to water in Arizona and evaluating its responses. If the model is not accurate, it needs to be retrained with additional data. Testing should be done using both automated and manual methods to ensure that the chatbot is providing accurate responses.

## Prompt Engineering

Prompt engineering is an essential component of ensuring that the chatbot can accurately and effectively respond to user queries. Prompt engineering involves crafting prompts in a way that helps the chatbot better understand the user's intent and provide relevant responses.

In more technical terms, prompt engineering involves designing the prompts in a way that provides the chatbot with more specific information about what the user is looking for, while also reducing the likelihood of misinterpretation. This can include using structured prompts that guide the user towards specific types of answers, or using natural language prompts that are designed to capture the user's intent more accurately.

The importance of prompt engineering can be understood by considering the complexity of natural language processing (NLP) and the limitations of current AI-powered chatbots. While AI-powered chatbots are becoming increasingly sophisticated, they still struggle with understanding context and ambiguity in language. This means that a chatbot may not always understand what a user is asking, or may provide irrelevant or incorrect responses.

Prompt engineering helps to overcome these limitations by providing the chatbot with more specific information about what the user is looking for. By crafting prompts in a way that more closely matches the user's intended meaning, prompt engineering can help to increase the accuracy and relevancy of a chatbot's responses. Furthermore, prompt engineering can help to reduce the amount of training data required for the chatbot, as it can help the chatbot to learn more efficiently from a smaller set of examples.

### How Does Prompt Engineering Work? 

Prompt engineering works by providing the chatbot with a set of prompts that are formulated in a way that matches the user's intended meaning. This can be achieved by analyzing the most common queries that users are likely to ask and designing prompts that are specifically tailored to those queries. The prompts can be designed using natural language processing techniques such as sentiment analysis, entity recognition, and intent classification to help identify the user's intent more accurately. 

### Different Types of Prompt Engineering

#### Structured Prompts 
Structured prompts are a type of prompt engineering technique that involves guiding the user towards specific types of answers. Structured prompts can be designed in a way that prompts the user to provide specific information in a certain order. For example, a chatbot designed to help users book flights may use structured prompts to ask the user for their departure location, destination, and travel dates in a specific order. This type of prompt engineering can help to reduce the likelihood of misinterpretation and increase the accuracy of the chatbot's responses. 

#### Natural Language Prompts 

Natural language prompts are a type of prompt engineering technique that involves designing prompts that are more closely matched to the user's intended meaning. Natural language prompts are designed to capture the user's intent more accurately and reduce the likelihood of misinterpretation. This type of prompt engineering can include using sentiment analysis, entity recognition, and intent classification to identify the user's intent more accurately. For example, a chatbot designed to help users find restaurants may use natural language prompts that are specifically tailored to different types of cuisines, such as "Find Italian restaurants near me." 

#### Multi-Step Prompts 

Multi-step prompts are a type of prompt engineering technique that involves breaking down complex queries into smaller, more manageable steps. This type of prompt engineering can help to reduce the likelihood of misinterpretation and increase the accuracy of the chatbot's responses. For example, a chatbot designed to help users troubleshoot technical issues may use multi-step prompts to guide the user through a series of questions to identify the root cause of the problem.

#### Adaptive Prompts 

Adaptive prompts are a type of prompt engineering technique that involves adjusting the prompts based on the user's previous responses. Adaptive prompts can be designed to ask follow-up questions based on the user's previous answers, thereby providing more specific information about what the user is looking for. For example, a chatbot designed to help users find a new car may use adaptive prompts to ask follow-up questions based on the user's preferred make and model.
### Benefits of Prompt Engineering 
There are several benefits to prompt engineering. Firstly, it can help to increase the accuracy and relevance of a chatbot's responses, thereby improving user satisfaction. Secondly, it can help to reduce the amount of training data required for the chatbot, which can result in faster and more efficient training. Finally, it can help to reduce the likelihood of misinterpretation of user queries, which can result in fewer errors and a better user experience.

### Limitations of Prompt Engineering 
While prompt engineering can be highly effective in aiding the development and training of chatbots, it does have some limitations. One of the main limitations is that it requires a significant amount of domain knowledge to design effective prompts. Additionally, it can be time-consuming and costly to develop and test a large number of prompts.
