import google.generativeai as genai
from PIL import Image
import textwrap
from pathlib import Path
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


model = genai.GenerativeModel("gemini-pro-vision")


def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title="Multilanguage Aadhar OCR")
st.header("Aadhar OCR LLM")

input_prompt = """
               You are an expert in understanding Passport.
               You will receive input images as Passport &
               you will have to answer questions based on the input image
               """

uploaded_file = st.file_uploader(
    "Choose an image...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the image")

prompt = """Analyze the provided image and extract comprehensive passport information. The extracted data should include the passport type, issuing country, passport number, holder's surname, holder's name, nationality, sex, date of birth, place of birth, date of issue, date of expiry, and place of issue. Please structure the extracted information in a JSON response with the following fields: type, country, number, surname, given_name, nationality, sex, date_of_birth, place_of_birth, date_of_issue, date_of_expiry, and place_of_issue. Ensure that the values for each field are accurately extracted from the image, particularly focusing on the details relevant to an Indian passport."""
# prompt = "Extract all Information such as Address, print_date from the Image and return it in JSON format"

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, prompt)
    st.subheader("The Response is")
    st.write(response)
