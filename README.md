# Backend for the Chatbot

https://hiring-assistant-omega.vercel.app/

## Project Outline

This is the assignment provided by PG-AGI, which is to create a Hiring Assistant that can collect information from user.
The information can include:
    - Name
    - E-mail
    - Phone Number
    - Current location
    - years of experience
    - desired position
    - Tech Stack
After collecting the information. The chatbot should ask 3-5 questions according to the tech stack.

## My Solution

### Tech Stack
I have used Flask for developing the backend and React.js for frontend for this project.
The reason why I am using these instead of Streamlit and Gradio is that Streamlit and Gradio does not host on a fixed url even on local deployment.
Therefore, In order to deploy the project on a fixed folder and for free I used Vercel. and since vercel did not support streamlit and gradio so used Flask for backend and React for frontend (https://github.com/mohit-ix/ChatBotFrontend).

### Installation Guide

Since this repository is for backend, so I will be explaining the installation for backend only.

```bash
pip install -r requirements.txt
```

After installing the requirements, create a .env file for storing groq key.
```python
"GROQ_API_KEY" = "Your api key"
```

Then use the following commands to run the server:
```bash
flask run
```

### Usage Guide

After the server is up and running. Run the host the frontend server as explained in https://github.com/mohit-ix/ChatBotFrontend and start using.

### Technical Details

*Model* I have used Groq api for free hosting of LLM model and the LLM model I am using is Llama 3.3 with 70 Billion parameters.
*Libraries* I am integrating the llm with langchain along with its memory checkpoint functionality to keep the flow of conversation. The chatbot always create a random thread Id to which keeps the conversation history in check. In this way multiple users can have conversation with the chatbot independently. Using this method, authorization and database can be added to keep the previous conversations saved.
*Architecture* Instead of using the traditional templating for webpage rendering, I have deployed Frontend and backend on different servers. When a user loads the website. A "Start" message is sent to the "/" route of flask, initiating the conversation first by the bot. Then all required information is asked from the user and finally the the conversation ends with "Goodbye" in the sentence. After this both input and send button are deactivated to not progress in the conversation.
At this point The conversation can be used to extract the necessary information accordingly.

### Prompt Design

First a personification is given to the LLM by asking it to "Assume you are a Hiring Assistant". Then the bot is asked to welcome the user on the keyword "Start".
All the required information can be collected now either one by one or it can be more than one field at once so as to not delay the process.
After collecting the information, the bot is to ask three question for each skill by emphasising with "at least" keyword.
The bot is asked to not get distracted from the conversation and console the user if they get nervous.
After all the information is collected the bot the bid farewell to the user with a "Goodbye".

### Challenges & Solutions

The most difficult challenge was to make the project with least amount of money. Because I have already used my free credits and trials of GCP, Azure, AWS and chatgpt api.
To face this challenge, instead of steamlit and gradio I used flask and react to deploy them to Vercel for free. And instead of Chatgpt API, I used Groq API for free while compromising the model with Llama instead of gpt-3/4.