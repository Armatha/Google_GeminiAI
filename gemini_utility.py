import os
import json
from http.client import responses

import google.generativeai as genai

working_directory=os.path.dirname(os.path.abspath(__file__))
config_file_path=f"{working_directory}/config.json"
config_data=json.load(open(config_file_path))
GOOGLE_API_KEY=config_data["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# model for chatbot
def load_gemini_pro_model():
    gemini_pro_model=genai.GenerativeModel("gemini-pro")
    return gemini_pro_model
# function for image vision
def gemini_vision(prompt,image):
    gemini_pro_vision_model=genai.GenerativeModel("gemini-1.5-flash")
    vision_response=gemini_pro_vision_model.generate_content([prompt,image])
    result=vision_response.text
    return result
# function for embedding text
def embed(input_text):
    embedding_model="models/text-embedding-004"
    embedd=genai.embed_content(model=embedding_model,content=input_text,task_type="retrieval_document")
    response=embedd["embedding"]
    return response
# out=embed("america")
# print(out)

# model for ask me any
def ask_me(prompt):
    askme_model=genai.GenerativeModel("gemini-pro")
    response=askme_model.generate_content(prompt)
    result=response.text
    return result