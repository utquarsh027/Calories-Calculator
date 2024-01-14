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
    prompt="""
""" Yoy are a nutritionist and given an uploaded image of a meal, calculate the calories for each individual food item present 
             and provide the results in separate lines. Additionally, include a line for the total calorie count 
             of the entire meal. Please specify any key factors affecting the calculation, such as portion size 
             or specific ingredients visible in the image. Ensure the calorie estimates are as accurate as 
             possible based on the visual information provided.
             Results should should be in the format 
             1. Item1- number of calories
                ----
                ----
             and so on"""

    generate=st.button("Calculate")
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

ft = """
<style>
a:link, a:visited {
  color: #BFBFBF;
  background-color: transparent;
  text-decoration: none;
}

a:hover, a:active {
  color: #0283C3;
  background-color: transparent;
  text-decoration: underline;
}

body {
  margin: 0;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content {
  flex: 1;
}

.footer {
  background-color: transparent;
  color: #808080;
  text-align: center;
  padding: 20px 0;
}
</style>

<div class="content">
  <!-- Your content here -->
</div>

<div class="footer">
  <p style='font-size: 0.875em;'>
    Made with <img src="https://em-content.zobj.net/source/skype/289/red-heart_2764-fe0f.png" alt="heart" height="10"/>
    <a href="https://github.com/utquarsh027" target="_blank">by Utkarsh</a>
  </p>
</div>
"""

st.write(ft, unsafe_allow_html=True)
