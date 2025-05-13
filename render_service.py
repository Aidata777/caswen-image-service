from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
import io

app = FastAPI()

def resize_and_crop(img: Image.Image, target_width: int, target_height: int) -> Image.Image:
    original_ratio = img.width / img.height
    target_ratio = target_width / target_height

    if original_ratio > target_ratio:
        new_height = target_height
        new_width = int(new_height * original_ratio)
    else:
        new_width = target_width
        new_height = int(new_width / original_ratio)

    img = img.resize((new_width, new_height), Image.LANCZOS)

    left = (new_width - target_width) / 2
    top = (new_height - target_height) / 2
    right = (new_width + target_width) / 2
    bottom = (new_height + target_height) / 2

    return img.crop((left, top, right, bottom))

@app.post("/generate/horizontal")
async def generate_horizontal(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    processed_image = resize_and_crop(image, 1200, 675)
    buffer = io.BytesIO()
    processed_image.save(buffer, format="JPEG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/jpeg")

@app.post("/generate/vertical")
async def generate_vertical(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    processed_image = resize_and_crop(image, 1080, 1350)
    buffer = io.BytesIO()
    processed_image.save(buffer, format="JPEG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/jpeg")

@app.post("/generate/square")
async def generate_square(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    processed_image = resize_and_crop(image, 1080, 1080)
    buffer = io.BytesIO()
    processed_image.save(buffer, format="JPEG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/jpeg")
