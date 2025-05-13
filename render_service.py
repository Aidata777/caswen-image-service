from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from PIL import Image
from io import BytesIO

app = FastAPI()

def resize_image(image: Image.Image, target_width: int, target_height: int) -> BytesIO:
    resized_image = image.resize((target_width, target_height), Image.LANCZOS)
    output = BytesIO()
    resized_image.save(output, format="PNG")
    output.seek(0)
    return output

@app.post("/generate/horizontal")
async def generate_horizontal(file: UploadFile = File(...)):
    image = Image.open(BytesIO(await file.read()))
    resized = resize_image(image, 1200, 628)
    return StreamingResponse(resized, media_type="image/png")

@app.post("/generate/vertical")
async def generate_vertical(file: UploadFile = File(...)):
    image = Image.open(BytesIO(await file.read()))
    resized = resize_image(image, 1080, 1350)
    return StreamingResponse(resized, media_type="image/png")

@app.post("/generate/square")
async def generate_square(file: UploadFile = File(...)):
    image = Image.open(BytesIO(await file.read()))
    resized = resize_image(image, 1080, 1080)
    return StreamingResponse(resized, media_type="image/png")

