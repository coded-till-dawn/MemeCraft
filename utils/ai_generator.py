import os
import replicate
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_meme_image(headline):
    """
    Uses Replicate's Flux 1.1 Pro model to generate a complete meme image.
    Returns a PIL Image object.
    """
    api_token = os.getenv("REPLICATE_API_TOKEN")
    if not api_token:
        raise ValueError("REPLICATE_API_TOKEN not found in .env file")

    # Prompt engineering for the meme template
    prompt = f"""
    A high-quality, blank meme template based on this description: "{headline}".
    Do NOT include any text on the image.
    The image should be a funny, viral-style scene suitable for a meme.
    High quality, sharp, colorful.
    """

    try:
        # Run the Flux 1.1 Pro model
        output = replicate.run(
            "black-forest-labs/flux-1.1-pro",
            input={
                "prompt": prompt,
                "aspect_ratio": "1:1",
                "output_format": "jpg",
                "output_quality": 90,
                "safety_tolerance": 2,
                "prompt_upsampling": True
            }
        )
        
        # The output is a FileOutput object which has a .read() method
        image_data = output.read()
        
        img = Image.open(BytesIO(image_data))
        return img

    except Exception as e:
        raise Exception(f"Flux Image generation failed: {e}")
