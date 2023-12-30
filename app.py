import streamlit as st 
from model import OpenAIBot, MessageItem
import os
st.set_page_config(page_title="Student Support Assistant", page_icon=":speech_balloon:")

st.title('Student Support Assistant')
st.write("You are a student support chatbot.")

# Create the "uploads" directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

# Create the file uploader
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    # Get the file name and save it to the "uploads" directory
    file_path = os.path.join("uploads", uploaded_file.name)
    # print(file_path)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

try:
    if "bot" not in st.session_state:
            st.session_state.bot = OpenAIBot("Student Support Assistant", 
                instructions="You are a student support chatbot.Use your knowledge base to best respond to student queries about Zia Ullah Khan.",
                file=file_path
                )

    for m in st.session_state.bot.getMessages():
        with st.chat_message(m.role):
            st.markdown(m.content)

    if prompt := st.chat_input("Please Ask a Question"):
        st.session_state.bot.send_message(prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        if(st.session_state.bot.isCompleted()):
            response: MessageItem = st.session_state.bot.get_lastest_response()
            with st.chat_message(response.role):
                st.markdown(response.content)
except:
    st.warning("Uploads Your PDF File To Start Discussion")