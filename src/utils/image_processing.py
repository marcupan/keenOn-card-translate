import requests
import io
from PIL import Image
from src.config import Config


def generate_image(prompt):
    api_key = Config.HUGGINGFACE_API_KEY
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"inputs": prompt}
    response = requests.post(
        "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        print(f"Failed to generate image: {response.status_code} {response.text}")
        return None

    image_data = response.content
    img = Image.open(io.BytesIO(image_data))
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io
