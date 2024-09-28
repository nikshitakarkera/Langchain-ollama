import subprocess
import base64
import speech_recognition as sr
import os
import webbrowser
import datetime
import random
import numpy as np
import win32com.client

import requests

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv

speaker = win32com.client.Dispatch("SAPI.SPvoice")

chatStr = ""


@st.experimental_memo
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64(r"C:\Users\NIKITHA\Downloads\Screenshot 2024-05-01 230318.png")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-color: ffffff;
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
st.sidebar.header("ABOUT THE MODEL")
st.sidebar.text("The Model used here is Neural-Chat. This project is implemented using Ollama ,Langchain and Streamlit")

st.sidebar.subheader("Neural-Chat Model :")
st.sidebar.text("Model Authors	Intel.")
st.sidebar.text("Core team members: Kaokao Lv, \n Liang Lv, Chang Wang, Wenxin\n Zhang, Xuhui Ren, and \nHaihao Shen.")
st.sidebar.text("Date	July, 2023")
st.sidebar.text("Version	v1-1")
st.sidebar.text("Type	7B Large Language Model")
st.sidebar.text("Base model: mosaicml/mpt-7b")
st.sidebar.text("Dataset: Intel/neural-chat-\ndataset-v1-1")
st.sidebar.text("License	Apache 2.0")


import requests

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

## Prompt Template

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please response to the user queries"),
        ("user","Question:{question}")
    ]
)


def chat(query):
    try:
        input_text=query

        # ollama LLAma2 LLm 
        llm=Ollama(model="neural-chat")
        output_parser=StrOutputParser()
        chain=prompt|llm|output_parser
        print("printing")

        if input_text:
            response_data=chain.invoke({"question":input_text})

        result = response_data
        #print(result)
        st.write(result)
        speaker.Speak(result)
        # Do something with the poem

    except Exception as e:
        print("Sorry - Something went wrong. Please try again!")
        st.write("Sorry - Something went wrong. Please try again!")


def ai(prompt, te_xt=None):
    input_text=prompt
    llm=Ollama(model="neural-chat")
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    print("printing")

    if input_text:
        response_data=chain.invoke({"question":input_text})

    result = response_data
    print(result)
    st.write(result)



def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold =  0.6
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            print("Recognizing...")
            st.write("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            st.subheader(f"User said: {query}")
            return query
        except Exception as e:
            st.write(f"Some Error Occurred. Sorry from Jarvis")
            return "Some Error Occurred. Sorry from Jarvis"

st.title('Welcome to Jarvis A.I')
print('Welcome to Jarvis A.I')
speaker.Speak("Jarvis A.I")

output_parser=StrOutputParser()

while True:
        print("Listening...")
        query = takeCommand()
        # todo: Add more sites
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"], ["spotify", "https://www.spotify.com"],
                 ["mail", "https://www.gmail.com"], ["instagram", "https://www.instagram.com"],
                 ["whatsapp", "https://web.whatsapp.com/"], ]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                speaker.Speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                st.divider()
        # todo: Add a feature to play a specific song
        if "open music" in query:
            spotify_exe = r"C:\Users\dell\AppData\Roaming\Spotify\Spotify.exe"
            subprocess.Popen([spotify_exe])
            st.divider()

        elif "open calculator" in query:
            calculator_exe = "calc.exe"  # Calculator executable name
            subprocess.Popen(calculator_exe)
            st.divider()

        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            speaker.Speak(f"Sir time is {hour} hours and {min} minutes")
            st.divider()


        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)
            st.divider()

        elif "Jarvis Quit".lower() in query.lower():
            speaker.Speak(f"exiting program sir")
            st.divider()
            break

        # elif "".lower() in query.lower():
        #     speaker.Speak(f"Sorry I could not understand")

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            st.write("Chatting...")
            chat(query)

        # say(query)