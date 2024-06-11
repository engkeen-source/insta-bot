import os
import subprocess
import json
import requests
from icecream import ic


class Dalle3_Engine():
    def __init__(self, prompt):
        self.api_key = os.environ.get('OPENAI_API_KEY')

        if self.api_key is None:
            raise ValueError("API Key is not set. Please set the OPENAI_API_KEY environment variable.")

        self.prompt = prompt
        self.img_dir = "images/"

        self.revised_prompt = None
        self.image_url = None

        self._generate_image()
        self._save_image()


    def _generate_image(self):

        # JSON data for the API request
        data = json.dumps({
            "model": "dall-e-3",          # Specifies the model to be used
            "prompt": self.prompt,        # The user-provided prompt
            "n": 1,                       # Number of images to generate
            "size": "1024x1024",          # Size of the generated images
            "quality": "hd",              # Optional: double cost for finer details & greater consistency
            "response_format": "url"      # Optional: url is default but b64_json is another option
        })

        # Constructing the cURL command for the API request
        curl_command = [
            "curl", "-X", "POST", "https://api.openai.com/v1/images/generations",
            "-H", "Content-Type: application/json",
            "-H", f"Authorization: Bearer {self.api_key}",
            "-d", data
        ]

        # Print the command for validation/debugging
        print("cURL Command:", " ".join(curl_command))
        
        # Executing the cURL command and capturing the response
        try:
            response = subprocess.run(curl_command, capture_output=True, text=True, check=True)
            print("Response:\n", response.stdout)
        except subprocess.CalledProcessError as e:
            # Handling errors during the API request
            print("Error occurred:")
            print(e.stderr)
            return

        # Parsing the JSON response
        response_json = json.loads(response.stdout)
        self.image_url = response_json['data'][0]['url']
        self.revised_prompt = response_json['data'][0]['revised_prompt']
            

    def _save_image(self):
        # Create the images directory if it doesn't exist
        if not os.path.exists(self.img_dir):
            os.makedirs(self.img_dir)

        # Construct the image path
        image_path = self.img_dir + self.prompt.replace(" ", "_") + ".png"
        image_path = image_path.lower()

        # Download the image
        response = requests.get(self.image_url)
        if response.status_code == 200:
            with open(image_path, 'wb') as file:
                file.write(response.content)
            print(f"Image saved at {image_path}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
