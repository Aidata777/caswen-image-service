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
    
    # Forzamos una relación de aspecto deseada
    target_ratio = width / height
    base_crop_width = image.width
    base_crop_height = int(base_crop_width / target_ratio)

    if base_crop_height > image.height:
        base_crop_height = image.height
        base_crop_width = int(base_crop_height * target_ratio)

    result = cropper.crop(image, base_crop_width, base_crop_height)

    box = (
        result['top_crop']['x'],
        result['top_crop']['y'],
        result['top_crop']['x'] + result['top_crop']['width'],
        result['top_crop']['y'] + result['top_crop']['height'],
    )

    cropped = image.crop(box)
    resized = cropped.resize((width, height), Image.LANCZOS)
    return resized

@app.post("/instagram")
async def render_instagram(file: UploadFile = File(...)):
    image = Image.open(file.file).convert("RGB")
    result = smart_crop_resize(image, 1080, 1350)
    output_path = os.path.join(OUTPUT_DIR, "instagram.jpg")
    result.save(output_path, "JPEG")
    return FileResponse(output_path, media_type="image/jpeg", filename="instagram.jpg")
