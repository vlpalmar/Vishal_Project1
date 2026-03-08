import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import gradio as gr

 
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

def echo(message, history):
    return "Gradio says: " + message

demo = gr.ChatInterface(chat, type="messages").launch()

if __name__ == "__main__":
    # Launch it, usually runs on port 7860
    demo.launch(server_port=7860)
Emb

import streamlit.components.v1 as components

st.title("Streamlit with Gradio Chatbot")

# Embed the Gradio App
components.iframe("http://localhost:7860", height=600)

