import base64
import streamlit as st
import openai
import requests
from PIL import Image
import os
# Set your OpenAI API key here
api_key = os.getenv('OPENAI_API_KEY')

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def save_uploaded_file(uploaded_file, target_path):
    with open(target_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

def app():
    st.title("Image Explanation Chatbot")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        save_uploaded_file(uploaded_file, 'temp.jpg')
        base64_image = encode_image('temp.jpg')
        headers = {
          "Content-Type": "application/json",
          "Authorization": f"Bearer {api_key}"
        }

        payload = {
                  "model": "gpt-4-vision-preview",
                  "messages": [
                    {
                      "role": "user",
                      "content": [
                        {
                          "type": "text",
                          "text": "What’s in this image? Explain the image content"
                        },
                        {
                          "type": "image_url",
                          "image_url": {
                          "url": f"data:image/jpeg;base64,{base64_image}"
                          }
                        }
                      ]
                    } 
                  ],
                  "max_tokens": 300
                }
        if st.button("Get Explanation"):
            try:
                # Call OpenAI API for image explanation
                # response = openai.Image.create(
                #     file=uploaded_file,
                #     model="text-davinci-003"
                # )

                # # Extract explanation from OpenAI API response
                # explanation = response['data'][0]['text']
                response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

                print(response.json())
                st.success("Explanation: {}".format(response.json()['choices'][0]['message']['content']))
            except Exception as e:
                st.error(f"Error: {e}")

