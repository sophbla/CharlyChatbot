import streamlit as st
from streamlit_chat import message
from PIL import Image
import requests

#Mainpage & Chatbot Section
st.set_page_config(
    page_title="Dr Genius - Demo site",
    page_icon=":heart:")

api_token = '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'
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Authorization": f"Bearer {api_token}"}

st.header("Welcome to Dr. Genius")


if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def get_text():
    input_text = st.text_input("You: ","Hi, I'd like some help!", key="input")
    return input_text


user_input = st.text_input("What would you like to talk about?")

if user_input:
    output = query({
        "inputs": {
            "past_user_inputs": st.session_state.past,
            "generated_responses": st.session_state.generated,
            "text": user_input,
        },"parameters": {"repetition_penalty": 1.33},
    })

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output["generated_text"])

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

#Sidebar section
image = "https://images.everydayhealth.com/images/how-to-find-a-therapist-whos-right-for-you-1440x810.jpg?w=1110"

with st.sidebar:

    #st.title("Welcome to Dr. Genius")

    st.image(image, caption='Fancy some therapy?')

    st.markdown("""
    -----------------------------------

    This chatbot was created by Le Wagon Students.
    It aims at acting as a *'virtual therapist'* anyone can talk to.

    To use the chatbot:
    - Type a sentence of your choice
    - Wait for Dr. Genius' answer
    - That's it!

    To learn more, visit our [Github Page]("https://github.com/sophbla/MHConvoAI").
""")

    "&nbsp;"

    expander = st.expander("Additional Resources & Info.")
    expander.write("""
    - [Replika.ai](https://https://replika.ai/)
    - [Wysa.io](https://https://www.wysa.io/)
    - [Online therapy](https://myonlinetherapy.com/)


    """)

    expander = st.expander("Disclaimer")
    expander.write("""
    *All content and information on this website if for informational and educational purposes only and does NOT constitute medical advice*.

""")


#st.write(st.session_state["generated"])

#st.write(output)

#st.write(st.session_state)

#st.write(st.session_state.past)
