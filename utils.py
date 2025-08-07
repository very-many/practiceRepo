import re
from io import BytesIO
from PIL import Image
import requests

def get_image_size(img_url):
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    return img.width, img.height

def create_svg_overlay(faces, img_width, img_height):
    rects = ""
    for face in faces:
        rect = face["faceRectangle"]
        rects += f'<rect x="{rect["left"]}" y="{rect["top"]}" width="{rect["width"]}" height="{rect["height"]}" fill="none" stroke="red" stroke-width="3"/>'
    svg = f"""
    <svg viewBox="0 0 {img_width} {img_height}" xmlns="http://www.w3.org/2000/svg"
         class="absolute inset-0 w-full h-full pointer-events-none">
        {rects}
    </svg>
    """
    return svg