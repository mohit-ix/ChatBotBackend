# Importing the dependencies
from flask import Flask, request
from flask_cors import CORS
import random
import json
from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

from langchain_core.messages import HumanMessage

# Creating a flask app
app = Flask(__name__)
# Enabling CORS for all requests
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Initializing the llama Model using Groq API
model = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")

# Initiating the prompt for system that will be used.
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            '''
            Assume you are a Hiring assistant from "TalentScout". I want you to perform specific tasks for me:
                - Welcome the user on the message "Start".
                - Ask for their Name, a valid email address, contact number, years of experience, desired position, current location and Tech stack turn by turn.
                - Ocassionaly ask for upto 3 relevant information at once.
                - Don't get distracted from the conversation.
                - After collecting the information, Ask the user 5 questions one by one for each skill mentioned in Tech Stack to test their knowledge.
                - If the user gets nervous then console them.
            After asking the questions. I want you to end the conversation with a "Goodbye".
            ''',
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Creating a graph according the text generation will be done
workflow = StateGraph(state_schema=MessagesState)

def call_model(state: MessagesState):
    '''
        This function accepts state varaible which is the message provided by user.
        This message will be passed to the prompt in graph which will then retrieve the response.
    '''
    prompt = prompt_template.invoke(state)
    response = model.invoke(prompt)
    return {"messages": response}

# Adding nodes and edges to the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Initiating a temporary memory which will story the history of conversation
memory = MemorySaver()
conversationModel = workflow.compile(checkpointer=memory)

# Generating a random thread Id which represents a different conversation in memory
threadId = str(random.randrange(0, 10000))

config = {"configurable": {"thread_id": threadId}}

# Endpoint for the conversation 
@app.route("/getResponse", methods=['POST'])
def getResponse():
    '''
        This function receives the message from user and provide it to the langchain graph for appropriate response.
        Then the reply is returned to the frontend in Json format:
        {
            "id": "A random id",
            "sender": "Bot for generated answer and user for user message",
            "text": "Generated message"
        }
    '''
    message = request.get_json()

    input_messages = [HumanMessage(message['message']['text'])]
    output = conversationModel.invoke({"messages": input_messages}, config)
    # print(output["messages"][-1].content)
    # output["messages"][-1].pretty_print()

    msgToSend = {
        "id": random.randrange(0, 10000),
        "sender": "bot",
        "text": output["messages"][-1].content
    }

    msgToSend = json.dumps(msgToSend)

    return msgToSend

# Endpoint for Initialization for the conversation
@app.route("/", methods=["POST"])
def index():
    '''
        This function receives "Start" from frontend and generate the Welcome message for User.
        Then the reply is returned to the frontend in Json format:
        {
            "id": "A random id",
            "sender": "Bot for generated answer and user for user message",
            "text": "Generated message"
        }
    '''
    message = request.get_json()

    input_messages = [HumanMessage(message['message']['text'])]
    output = conversationModel.invoke({"messages": input_messages}, config)
    # print(output["messages"][-1].content)
    # output["messages"][-1].pretty_print()

    msgToSend = {
        "id": random.randrange(0, 10000),
        "sender": "bot",
        "text": output["messages"][-1].content
    }

    msgToSend = json.dumps(msgToSend)

    return msgToSend