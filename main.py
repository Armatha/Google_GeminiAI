import os
from PIL import Image
import streamlit as st
from streamlit import chat_message
from streamlit_option_menu import option_menu
from gemini_utility import (load_gemini_pro_model,
                            gemini_vision,
                            embed,
                            ask_me)

working_directory=os.path.dirname(os.path.abspath(__file__))
# print(working_directory)

st.set_page_config(
    page_title="Gemini AI",
    page_icon="🧠",
    layout="centered"
)

with st.sidebar:
    selected=option_menu("Gemini AI",
                         ["Chatbot",
                          "Image Captioning",
                          "Embed Text",
                          "Ask me Anything"],
                         menu_icon="robot",
                         icons=["chat-dots-fill","image-fill",
                         "file-text-fill","question-octagon-fill"],
                         default_index=0)

def translate_role_user(user_role):
    if user_role=='model':
        return "assistant"
    else:
        return user_role

if selected=="Chatbot":
    st.title('🤖 robot')

    model=load_gemini_pro_model()

    if "chat_session" not in st.session_state:
        st.session_state.chat_session=model.start_chat(history=[])

    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_user(message.role)):
            st.markdown(message.parts[0].text)

    user_prompt=st.chat_input("Ask me anything....")
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        gemini_response=st.session_state.chat_session.send_message(user_prompt)
        # display gemini response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

if selected=="Image Captioning":
    st.title("📷Image caption")
    uploaded_img=st.file_uploader("upload image",type=["jpg","png"])
    image=Image.open(uploaded_img)
    prompt="w"
    if st.button("Generate caption"):
        col1,col2=st.columns(2)
        with col1:
            resized_img=image.resize((800,500))
            st.image(resized_img)
        with col2:
            caption=gemini_vision(prompt,image)
            st.info(caption)

if selected=="Embed Text":
    st.title("🔡 Embedd Text")
    input_text=st.text_area(label="",placeholder="Type your text here..")
    if st.button("Embedd Text"):
        out=embed(input_text)
        st.markdown(out)

if selected=="Ask me Anything":
    st.title("? Ask me Anything")
    prompt=st.text_area(label="",placeholder="ask me anything..")
    if st.button("Get answer"):
        response=ask_me(prompt)
        st.markdown(response)