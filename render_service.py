from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from PIL import Image
import smartcrop
import os

app = FastAPI()
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def smart_crop_resize(image: Image.Image, width: int, height: int) -> Image.Image:
    cropper = smartcrop.SmartCrop()
    target_ratio = width / height

    # Paso 1: pedir sugerencia inteligente
    result = cropper.crop(image, width, height)
    box = result['top_crop']

    # Paso 2: si el recorte sugerido es casi igual al tamaño original, forzar recorte centrado
    if box['width'] >= image.width * 0.98 and box['height'] >= image.height * 0.98:
        original_ratio = image.width / image.height
        if original_ratio > target_ratio:
            # Imagen más ancha que deseado: recortar laterales
            new_width = int(image.height * target_ratio)
            left = (image.width - new_width) // 2
            box_coords = (left, 0, left + new_width, image.height)
        else:
            # Imagen más alta que deseado: recortar arriba y abajo
            new_height = int(image.width / target_ratio)
            top = (image.height - new_height) // 2
            box_coords = (0, top, image.width, top + new_height)
    else:
        # Usar recorte propuesto por smartcrop
        box_coords = (
            box['x'],
            box['y'],
            box['x'] + box['width'],
            box['y'] + box['height']
        )

    cropped = image.crop(box_coords)
    resized = cropped.resize((width, height), Image.LANCZOS)
    return resized

@app.post("/instagram")
async def render_instagram(file: UploadFile = File(...)):
    image = Image.open(file.file).convert("RGB")
    result = smart_crop_resize(image, 1080, 1350)
    output_path = os.path.join(OUTPUT_DIR, "instagram.jpg")
    result.save(output_path, "JPEG")
    return FileResponse(output_path, media_type="image/jpeg", filename="instagram.jpg")

