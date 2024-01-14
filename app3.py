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
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----


"""
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
