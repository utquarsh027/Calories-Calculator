import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm
from PIL import Image


API_KEY="AIzaSyAo9yfpvJACfzgxPyX3cj3FkSoV4wUy3nY"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Calories Calculator", 
                   page_icon="🔥",
                   layout="centered",
                   initial_sidebar_state='collapsed')

st.header("Calories Calculator")
uploaded_file = st.file_uploader("Upload an Image file", accept_multiple_files=False, type=['jpg', 'png','jfif'])
if uploaded_file is not None:
    image = Image.open(uploaded_file)

    st.image(image, caption='Uploaded Image', use_column_width=True)
    bytes_data = uploaded_file.getvalue()
    prompt="Given an uploaded image of a meal, calculate the calories and protein content for each individual food item present, and provide the results in separate lines. Additionally, include a line for the total calorie count and total protein content of the entire meal.Ensure the calorie and protein estimates are as accurate as possible based on the visual information provided."
    generate=st.button("Generate")
    if generate:
        try:
            model = genai.GenerativeModel('gemini-pro-vision')
            response = model.generate_content(
            glm.Content(
                    parts = [
                        glm.Part(text=prompt),
                        glm.Part(
                            inline_data=glm.Blob(
                                mime_type='image/jpeg',
                                data=bytes_data
                            )
                        ),
                    ],
                ),
                stream=True)

            response.resolve()
            st.write(response.text)
        except:
            st.write("Error!Check the prompt or uploaded image")
