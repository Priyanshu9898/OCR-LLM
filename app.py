from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
from typing import Optional
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
from pydantic import BaseModel, Field
from fastapi import HTTPException

class AadharInfo(BaseModel):
    name: str = Field(..., example="Malaviya Priyanshu Rajeshbhai")
    dob: str = Field(..., example="22/08/2001")
    gender: str = Field(..., example="Male")
    aadhar_number: str = Field(..., example="326766239712")
    issue_date: str = Field(..., example="18/01/2014")

app = FastAPI()
load_dotenv()

# Configure Google API
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro-vision")


def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_setup(uploaded_file: UploadFile) -> list:
    bytes_data = uploaded_file.file.read()
    image_parts = [
        {
            "mime_type": uploaded_file.content_type,
            "data": bytes_data
        }
    ]
    return image_parts


@app.post("/process-front/", summary="Process Aadhar Image Frontside",
          responses={400: {"description": "Bad Request - Non-JSON or Invalid JSON response"}})
async def process_image(uploaded_file: UploadFile = File(...)):
    
    """
    Extracts information from an Aadhar card image.

    This endpoint takes an Aadhar card image as input and uses a generative AI model to extract information such as name, date of birth, gender, Aadhar number, and issue date.

    - **uploaded_file**: Image file of an Aadhar card.
    """
    
    
    input_prompt = """
    You are an expert in understanding Aadhar Card.
    You will receive input images as Aadhar Card &
    you will have to answer questions based on the input image
    """
    prompt = """Extract all Information such as Name, DOB, Gender, Aadhar_Number and issue_date from the Image and return it in JSON format"""

    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, prompt)

        print(f"Response type: {type(response)}")

        # Debug: Print the raw response
        print(f"Raw response: {response}")

        cleaned_response = response.replace(
            "```json\n", "").replace("\n```", "").strip()

        if cleaned_response.startswith(('{', '[')):
            parsed_response = json.loads(cleaned_response)
            return JSONResponse(content=parsed_response)
        else:
            return JSONResponse(status_code=400, content={"message": "Received non-JSON response", "response": cleaned_response})
    except json.JSONDecodeError as json_error:
        return JSONResponse(status_code=400, content={"message": "Failed to parse JSON response", "error": str(json_error)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
    
@app.post("/process-back/", summary="Process Aadhar Image Backside",
          responses={400: {"description": "Bad Request - Non-JSON or Invalid JSON response"}})
async def process_image(uploaded_file: UploadFile = File(...)):
    
    """
    Extracts information from an Aadhar card image.

    This endpoint takes an Aadhar card image as input and uses a generative AI model to extract information such as name, date of birth, gender, Aadhar number, and issue date.

    - **uploaded_file**: Image file of an Aadhar card.
    """
    
    
    input_prompt = """
    You are an expert in understanding Aadhar Card.
    You will receive input images as Aadhar Card &
    you will have to answer questions based on the input image
    """
    prompt = "Extract all Information such as Address, print_date from the Image and return it in JSON format"

    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, prompt)

        print(f"Response type: {type(response)}")

        # Debug: Print the raw response
        print(f"Raw response: {response}")

        cleaned_response = response.replace(
            "```json\n", "").replace("\n```", "").strip()

        if cleaned_response.startswith(('{', '[')):
            parsed_response = json.loads(cleaned_response)
            return JSONResponse(content=parsed_response)
        else:
            return JSONResponse(status_code=400, content={"message": "Received non-JSON response", "response": cleaned_response})
    except json.JSONDecodeError as json_error:
        return JSONResponse(status_code=400, content={"message": "Failed to parse JSON response", "error": str(json_error)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
    
    




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
