import streamlit as st
import requests
from pydantic import BaseModel
from PIL import Image,ImageDraw
import pyttsx3

engine = pyttsx3.init()
# Define the data model for the request and response
class QueryRequest(BaseModel):
    user_input: str

class QueryResponse(BaseModel):
    bot_response: str
    manual_text: str

# Set the base URL of the API endpoint
BASE_URL = "127.0.0.1:8000"

# Function to convert text to speech
def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()
   
    
# Define a function to generate a response from the API
def generate_response(user_input):
    request_payload = QueryRequest(user_input=user_input)

    response = requests.post(f"http://{BASE_URL}/query-request", json=request_payload.dict())

    if response.status_code == 200:
        query_response = response.json()
    else :
        query_response = ["Error processing request" , "--empty--"]
    return [query_response["bot_response"] , query_response["manual_text"]]
    
#-------------------------------------Picture Uploading---------------------------------
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

target_type = st.text_input("Target Object:","")
if uploaded_file is not None:
    with Image.open(uploaded_file) :
        st.image(uploaded_file)
send_image = st.button("Send image")
if uploaded_file is not None and send_image:
    # Prepare the data to send
    payload = {"image": uploaded_file}
    # Send the POST request to the endpoint
    response = requests.post(f"http://{BASE_URL}/upload-image?target={target_type}", files=payload)
    if response.status_code == 200:
        # Decode the image from the response
        response_data = response.json()
        message = response_data["adjust"]
        # Decode the base64 image string to bytes
        pil_image = Image.open(uploaded_file)
        draw = ImageDraw.Draw(pil_image)
        for bounding_box in response_data['response'] :
            if bounding_box[0] == target_type :
                xmid = bounding_box[1]
                ymid = bounding_box[2]
                w =  bounding_box[3]
                h =  bounding_box[4]
                xmin = xmid - w/2
                ymin = ymid - h/2
                xmax = xmid + w/2
                ymax = ymid + h/2
                draw.rectangle([(xmin, ymin), (xmax, ymax)], outline=(0, 255, 0), width=5)
        st.image(pil_image)
        st.text(message)   
    else :
        st.text("Failed to get response")
#---------------------------------------------------ChatBot-----------------------------------------------

# Set the title and header of the web page
st.title("AssistBot")
st.header("Welcome ! how may I help you ?")

# Add a text input area for the user to enter their message
user_input = st.text_input(">>", "")

# Add a button to submit the user's message
submit_button = st.button('Write')
speak_button =  st.button('Speak')
# When the submit button is clicked, generate a response and display it
if submit_button:
    response = generate_response(user_input)
    st.text_area("AssistBot", value=response[0], height=100)
    st.text_area("Used Context: ", value= response[1] , height=200)

    
if speak_button:
    response = generate_response(user_input)
    st.text_area("AssistBot", value=response[0], height=100)
    st.text_area("Used Context: ", value= response[1] , height=200)
    text_to_speech(response[0])
    
    
       

