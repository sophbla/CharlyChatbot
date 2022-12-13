import streamlit as st
from streamlit_chat import message
from PIL import Image
import requests
import re


#Setting session_states
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'collapsed'

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'history' not in st.session_state:
    st.session_state['history'] = []

#Header
st.set_page_config(
    page_title = 'Dr. Genius',
    page_icon=":heart:",
    initial_sidebar_state=st.session_state.sidebar_state)

#Sidebar and Refresh
f1, f2 = st.columns([1, 0.16])
with f1:
    #Side bar button
    if st.button('Click for more resources'):
        st.session_state.sidebar_state = 'expanded' if st.session_state.sidebar_state == 'collapsed' else 'collapsed'
        # Force an app rerun after switching the sidebar state.
        st.experimental_rerun()
with f2:
    if st.button('Refresh'):
        st.session_state['generated'] = []
        st.session_state['past'] = []
        st.session_state['history'] = []

st.title('Welcome to Dr.Genius')


#API
# api_token = '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'
API_URL = "https://mhconvoai-kk3ee7qoyq-ew.a.run.app/predict"
# headers = {"Authorization": f"Bearer {api_token}"}

#API Functions
def query(params):
	response = requests.get(API_URL, params=params)
	return response.json()

def get_text():
    input_text = st.text_input("You: ","Hi, I'd like some help!", key="input")
    return input_text

# Chat input from User
user_input = st.text_input("What would you like to talk about?")

#Set history for query
history = st.session_state.history
# st.write(history)

#Making request, getting response
if user_input:
    output = query(params= {
        "text": user_input,
        "history": history
        })
    # st.write(output)

    st.session_state.history = output['new_history']
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output['output'])

#Displaying as chat
if st.session_state['generated']:

    for i in range(0, len(st.session_state['generated'])):
        output_message = re.sub(r'<.*?>', '', st.session_state['generated'][i])
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(output_message, key=str(i))

# st.write(st.session_state.past)
# st.write(st.session_state.generated)


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
