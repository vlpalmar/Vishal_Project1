import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
#import gradio as gr

 
#For running remotely use this to get api 
api_key = st.secrets['OPENAI_API_KEY']

# Check the key
if not api_key:
    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
elif not api_key.startswith("sk-proj-"):
    print("An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
elif api_key.strip() != api_key:
    print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
else:
    print("API key found and looks good so far!")

openai = OpenAI()

reader = PdfReader("linkedin.pdf")
linkedin = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        linkedin += text

with open("summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()

name = "Vishal Palmar"

system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer, say so."

system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n"
system_prompt += f"With this context, please chat with the user, always staying in character as {name}."

def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
    return response.choices[0].message.content

#st.write(name)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content": system_prompt})

# Display chat messages from history
#for message in st.session_state.messages:
    #with st.chat_message(message["role"]):
        #st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("Say something"):
    # Add user message to chat history and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        # Use st.write_stream for a ChatGPT-like streaming effect
        stream = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True, # Enable streaming
        )
        response = st.write_stream(stream)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})


#gr.ChatInterface(chat, type="messages").launch()

