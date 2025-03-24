import os
import base64
import openai
from flask import  request, jsonify
from dotenv import load_dotenv
# from PIL import Image

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class ImageDetection():
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
        
    def process_image():
        if 'image' not in request.files or 'violation_type' not in request.form:
            return jsonify({"error": "Image file and violation type are required"}), 400

        image_file = request.files['image']
        violation_type = request.form['violation_type']

        # Save the uploaded image
        image_path = "uploaded_image.jpg"
        image_file.save(image_path)

        # Encode image to base64
        image_base64 = ImageDetection.encode_image(image_path)

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an AI that detects traffic rule violations in images."},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": f"Check if the image contains a vehicle. If yes, check for the following violation: {violation_type}. If a violation is found, extract the vehicle number if possible. Respond with 'No vehicle detected' if no vehicle is found. Respond with 'No violation found' if no rule is broken. If no number plate is visible, return 'No number found'."},
                            {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_base64}"}
                        ]
                    }
                ],
                max_tokens=200
            )

            result = response["choices"][0]["message"]["content"]
            return jsonify({"result": result})

        except Exception as e:
            return jsonify({"error": str(e)}), 500