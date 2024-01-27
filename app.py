from flask import Flask, request, jsonify
from flask_cors import cross_origin
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure Google API
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro-vision")

app = Flask(__name__)
# Define allowed origins for CORS
allowed_origins = ["http://localhost:3000", "http://127.0.0.1:3000", "https://erphome.azurewebsites.net/auth/login", "https://erphome.azurewebsites.net"]


CORS(app, resources={r"/*": {"origins": allowed_origins}})


SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_setup(uploaded_file):
    bytes_data = uploaded_file.read()
    image_parts = [
        {
            "mime_type": uploaded_file.content_type,
            "data": bytes_data
        }
    ]
    return image_parts


@app.route('/aadhar-front/', methods=['POST'])
@cross_origin(origins=allowed_origins)
def process_front_image():
    if 'uploaded_file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['uploaded_file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file:
        input_prompt = """
    You are an expert in understanding Aadhar Card.
    You will receive input images as Aadhar Card &
    you will have to answer questions based on the input image
    """
        prompt = "Extract 'Name', 'DOB', 'Gender', 'Aadhar_Number', and 'issue_date' from the image. Return the information in JSON format with corresponding fields."
        try:
            image_data = input_image_setup(file)
            response = get_gemini_response(input_prompt, image_data, prompt)
            cleaned_response = response.replace(
                '```json\n', '').replace('\n```', '').strip()
            if cleaned_response.startswith(('{', '[')):
                parsed_response = json.loads(cleaned_response)
                return jsonify(parsed_response)
            else:
                return jsonify({"message": "Received non-JSON response", "response": cleaned_response}), 400
        except json.JSONDecodeError as json_error:
            return jsonify({"message": "Failed to parse JSON response", "error": str(json_error)}), 400
        except Exception as e:
            return jsonify({"message": str(e)}), 500


@app.route('/aadhar-back/', methods=['POST'])
@cross_origin(origins=allowed_origins)
def process_back_image():
    if 'uploaded_file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['uploaded_file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file:
        input_prompt = """
    You are an expert in understanding Aadhar Card.
    You will receive input images as Aadhar Card &
    you will have to answer questions based on the input image
    """
        prompt = "Analyze the attached image and extract 'Address' and 'print_date'. Format the extracted data into a JSON response with fields for Address and print_date."
        try:
            image_data = input_image_setup(file)
            response = get_gemini_response(input_prompt, image_data, prompt)
            cleaned_response = response.replace(
                '```json\n', '').replace('\n```', '').strip()
            if cleaned_response.startswith(('{', '[')):
                parsed_response = json.loads(cleaned_response)
                return jsonify(parsed_response)
            else:
                return jsonify({"message": "Received non-JSON response", "response": cleaned_response}), 400
        except json.JSONDecodeError as json_error:
            return jsonify({"message": "Failed to parse JSON response", "error": str(json_error)}), 400
        except Exception as e:
            return jsonify({"message": str(e)}), 500


@app.route('/passport-front/', methods=['POST'])
@cross_origin(origins=allowed_origins)
def process_passport_front_image():
    if 'uploaded_file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['uploaded_file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file:
        input_prompt = """You are an expert in understanding Passport. You will receive input images as Passport & you will have to answer questions based on the input image"""
        prompt = """Analyze the provided image and extract comprehensive passport information. The extracted data should include the passport type, issuing country, passport number, holder's surname, holder's name, nationality, sex, date of birth, place of birth, date of issue, date of expiry, and place of issue. Please structure the extracted information in a JSON response with the following fields: type, country, number, surname, given_name, nationality, sex, date_of_birth, place_of_birth, date_of_issue, date_of_expiry, and place_of_issue. Ensure that the values for each field are accurately extracted from the image, particularly focusing on the details relevant to an Indian passport."""
        try:
            image_data = input_image_setup(file)
            response = get_gemini_response(input_prompt, image_data, prompt)
            cleaned_response = response.replace(
                '```json\n', '').replace('\n```', '').strip()
            if cleaned_response.startswith(('{', '[')):
                parsed_response = json.loads(cleaned_response)
                return jsonify(parsed_response)
            else:
                return jsonify({"message": "Received non-JSON response", "response": cleaned_response}), 400
        except json.JSONDecodeError as json_error:
            return jsonify({"message": "Failed to parse JSON response", "error": str(json_error)}), 400
        except Exception as e:
            return jsonify({"message": str(e)}), 500


@app.route('/passport-back/', methods=['POST'])
@cross_origin(origins=allowed_origins)
def process_passport_back_image():
    if 'uploaded_file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['uploaded_file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file:
        input_prompt = """You are an expert in understanding Passport. You will receive input images as Passport & you will have to answer questions based on the input image"""
        prompt = """After analyzing the image, format the extracted information into a structured JSON response that includes fields for father_name, mother_name, spouse_name, address, old_passport_number and file_number."""
        try:
            image_data = input_image_setup(file)
            response = get_gemini_response(input_prompt, image_data, prompt)
            cleaned_response = response.replace(
                '```json\n', '').replace('\n```', '').strip()
            if cleaned_response.startswith(('{', '[')):
                parsed_response = json.loads(cleaned_response)
                return jsonify(parsed_response)
            else:
                return jsonify({"message": "Received non-JSON response", "response": cleaned_response}), 400
        except json.JSONDecodeError as json_error:
            return jsonify({"message": "Failed to parse JSON response", "error": str(json_error)}), 400
        except Exception as e:
            return jsonify({"message": str(e)}), 500


@app.route('/')
@cross_origin(origins=allowed_origins)
def index():
    return "<h1>Aadhar OCR Backend</h1> <br /> Go to Swagger Docs: <a href='/swagger'>Link</a>"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
