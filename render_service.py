from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import StreamingResponse
from PIL import Image
from io import BytesIO

app = FastAPI()

def resize_image(img: Image.Image, target_size: tuple) -> BytesIO:
    img_resized = img.copy()
    img_resized.thumbnail(target_size, Image.Resampling.LANCZOS)
    output = BytesIO()
    img_resized.save(output, format="PNG")
    output.seek(0)
    return output

@app.post("/generate/horizontal")
async def generate_horizontal(file: UploadFile, text: str = Form(...)):
    original_image = Image.open(BytesIO(await file.read()))
    resized_io = resize_image(original_image, (1200, 675))  # Horizontal 16:9
    return StreamingResponse(resized_io, media_type="image/png")

@app.post("/generate/vertical")
async def generate_vertical(file: UploadFile, text: str = Form(...)):
    original_image = Image.open(BytesIO(await file.read()))
    resized_io = resize_image(original_image, (720, 1280))  # Vertical 9:16
    return StreamingResponse(resized_io, media_type="image/png")

@app.post("/generate/square")
async def generate_square(file: UploadFile, text: str = Form(...)):
    original_image = Image.open(BytesIO(await file.read()))
    resized_io = resize_image(original_image, (1080, 1080))  # Square 1:1
    return StreamingResponse(resized_io, media_type="image/png")
