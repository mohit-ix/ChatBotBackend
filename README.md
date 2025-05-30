# Backend for the Chatbot

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
"GROQ_API_KEY" = "Your api key"

Then use the following commands to run the server:
```bash
flask run
```