import os
import base64
import openai
from flask import  request, jsonify
from dotenv import load_dotenv
import json
from Models.user_model import User

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class ImageDetection():
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
        
    def process_image():
        if 'image' not in request.files:
            return jsonify({"error": "Image file is required"}), 400

        image_file = request.files['image']

        image_path = "uploaded_image.jpg"
        image_file.save(image_path)

        image_base64 = ImageDetection.encode_image(image_path)

        try:
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an AI that detects traffic rule violations in images."},
                    {
                        "role": "user",
                        "content": [
                            {"type": f"text", "text": 'Analyze the image and check for any traffic rule violations, such as not wearing a helmet, using a mobile phone while driving, or more than two people on a two-wheeler. If violations are found give it in single string and If a vehicle number plate is visible, extract and return the number in the formate of json {"message":"give all the violations","vehicle_number":"if number found else give null"}. If no violations are found, return {"message":"No violation detected"}. If no vehicle number is found, return {"message":"No number found"}. '},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                        ]
                    }
                ],
                max_tokens=300
            )

            result = response.choices[0].message.content
            try:
                results = json.loads(result)
                if 'vehicle_number' in result:
                    user = User.objects(vehicle_no=results.get('vehicle_number')).first()
                    if user:
                        fine = (user.fine or 0) + 800 
                        user.update(fine=fine)
                        user.save()
                return jsonify({"result": results}),200
            except Exception as e:
                return jsonify({f"Exception Occured {str(e)}": result}),400
                
        except Exception as e:
            return jsonify({"error": str(e)}), 500
