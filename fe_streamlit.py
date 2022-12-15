import streamlit as st
from streamlit_chat import message
from PIL import Image
import requests
import re

#Setting session_states
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'expanded'

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'history' not in st.session_state:
    st.session_state['history'] = []

#Header
st.set_page_config(
    page_title = 'Charly',
    page_icon=":sun_behind_cloud:",
    initial_sidebar_state=st.session_state.sidebar_state)

#Sidebar and Refresh buttons style
m = st.markdown("""
<style>
div.stButton > button:first-child {
    height: 2em;
    width:6em;
    border-radius:5px;
    border:1px solid #000000;
    font-size:25px;
    font-weight: bold;
    display: block;
}

div.stButton > button:hover {
 background-color: #ECF5ED;
 color: black;
 border:2px solid #000000;
 font-weight: bold;
}

div.stButton > button:active {
	position:relative;
    border:2px solid #000000;
	top:2px;
}

</style>""", unsafe_allow_html=True)


f1, f2 = st.columns([3,0.85])
with f1:
    #Side bar button
    if st.button('Toggle sidebar'):
        st.session_state.sidebar_state = 'expanded' if st.session_state.sidebar_state == 'collapsed' else 'collapsed'
        # Force an app rerun after switching the sidebar state.
        st.experimental_rerun()
with f2:
    if st.button('Clear chat'):
        st.session_state['generated'] = []
        st.session_state['past'] = []
        st.session_state['history'] = []

#Welcome message / title
st.title("Hi, I'm Charly! ")


#API
API_URL = "https://mhconvai-full-kk3ee7qoyq-ew.a.run.app/predict"


#API Functions
def query(params):
	response = requests.get(API_URL, params=params)
	return response.json()

def get_text():
    input_text = st.text_input("You: ","Hi, I'd like some help!", key="input")
    return input_text

# Chat input from User
user_input = st.text_input("What would you like to chat about?")

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
        message(st.session_state['past'][i], avatar_style='micah', seed = 45, is_user=True, key=str(i) + '_user')
        message(output_message, avatar_style='croodles-neutral', seed = 45, key=str(i))



#####################
####### Sidebar content
#####################

image = 'https://i.postimg.cc/cLbyPzKz/logo-chat-1.png'
# In case our logo hosting is KO, use "https://images.everydayhealth.com/images/how-to-find-a-therapist-whos-right-for-you-1440x810.jpg?w=1110"


with st.sidebar:

    st.image(image,width=100,use_column_width='auto')



    #####################
    ####### Expanders
    #####################
    st.markdown("""
    Additional resources :point_down:
    """)
    expander = st.expander("Crisis hotlines Info")
    expander.write(""" These hotlines are for anyone who's struggling. They won't judge you. Free, anonymous, and always open.
    - **Samaritans** | Phone: 116 123 - [https://www.samaritans.org](https://www.samaritans.org)
    - **SHOUT** | Text: 85258 - [https://giveusashout.org](https://giveusashout.org)

    """)

    expander = st.expander("Information and support")
    expander.write(""" If you are living with a mental health issue or supporting someone who is, having access to the right information is vital.
    - **Mind** | [https://www.mind.org.uk](https://www.mind.org.uk)
    - **NHS** | [https://www.nhs.uk/mental-health](https://www.nhs.uk/mental-health)

    """)

    #####################
    ####### Text info
    #####################

    st.markdown("""
    -----------------------------------
    This chatbot was created by Le Wagon Students.
    It's a *virtual companion* anyone can talk to.
    To chat with Charly:
    - Type a sentence of your choice
    - Wait for Charly's answer
    - That's it!
    To learn more, visit our [Github Page](https://github.com/sophbla/CharlyChatbot.git).



    """)

    #####################
    ####### Disclaimer style & content
    #####################
    st.markdown(""" <style> .disclaimer {
    font-size: 10px; color: #999999;font-style: italic}
    </style> """, unsafe_allow_html=True)

    st.markdown("""<p class='disclaimer'>
    Disclaimer: All content and information on this website if for informational and educational purposes only and does NOT constitute medical advice.
    </p>""", unsafe_allow_html=True)





#st.write(st.session_state["generated"])
#st.write(output)
#st.write(st.session_state)
#st.write(st.session_state.past)
