import os
import streamlit as st
from dotenv import load_dotenv
#from scraper import fetch_website_contents
#from IPython.display import Markdown, display
from openai import OpenAI

#load_dotenv(override=True)
#api_key = os.getenv('OPENAI_API_KEY')

#For running remotely use this to get api key
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


# @st.dialog("User Input Form")
# def user_form_dialog():
# global UserQuery
# UserQuery = st.text_input("Your Query")
# #age = st.number_input("Age", min_value=0, max_value=120)
# if st.button("Submit"):
# st.session_state["submitted_UserQuery"] = UserQuery
# #st.session_state["submitted_age"] = age
# st.rerun() # To close the dialog and update the main app

#if "submitted_name" in st.session_state:
#st.write(f"Name: {st.session_state['submitted_name']}, Age: {st.session_state['submitted_age']}")

st.title("AI Model")

openai = OpenAI()
#To get the response from AI model and return the response
def getResponse(user_input):
 messages = [{"role": "user", "content": user_input}]
 response = openai.chat.completions.create(model="gpt-5-nano", messages=messages)
 return response.choices[0].message.content

user_input = st.text_input("Enter your prompt and press enter")
if user_input:
 response = getResponse(user_input)

 st.write(response)
