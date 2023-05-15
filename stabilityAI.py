from flask import Flask, jsonify, request
from flask_cors import CORS 
import base64
import os
import requests


engine_id = "stable-diffusion-v1-5"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
api_key = ("sk-KGvr7LUYDIXrR78zGk2o31RhJGW4op48qrCM0GAhlWYuTH7N")

img_pth = os.path.join(os.getcwd(), "v1_txt2img.png")

def gen_img(textt):
    if api_key is None:
        raise Exception("Missing Stability API key.")

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": textt
                }
            ],
            "cfg_scale": 7,
            "clip_guidance_preset": "FAST_BLUE",
            "height": 512,
            "width": 512,
            "samples": 1,
            "steps": 30,
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    for i, image in enumerate(data["artifacts"]):
    	with open(img_pth, "wb") as f:
    		f.write(base64.b64decode(image["base64"]))
    		

    
    # Set up the necessary variables for GitHub
    repo_owner = "DevTimlas"
    repo_name = "stabilityAPI"  # The name of the repository
    file_path = "images/v1_txt2img.png"  # The path where you want to save the image in the repository
    access_token = "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"  # Your GitHub access token

    # Read the image file
    with open(img_pth, "rb") as file:
        image_data = file.read()

    # Encode the image data as base64
    encoded_image = base64.b64encode(image_data).decode("utf-8")

    # Set up the API URL
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"

    # Set up the request headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Set up the request payload
    payload = {
        "message": "Add image",
        "content": encoded_image
    }

    # Make the API request
    response = requests.put(url, json=payload, headers=headers)

    # Check the response status
    if response.status_code == 201:
        print("Image saved successfully!")
    else:
        print(f"Failed to save the image. Status code: {response.status_code}")
        print(response.json())

    return ('image saved...')

  
app = Flask(__name__)
CORS(app)

@app.route('/generate', methods=['POST'])
def index():
    user_input = request.json['user_input']
    res = str(gen_img(user_input))
    return jsonify({'msg': res})
