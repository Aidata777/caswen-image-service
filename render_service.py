from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from PIL import Image
from io import BytesIO

app = FastAPI()

def resize_image(img: Image.Image, target_width: int, target_height: int) -> Image.Image:
    return img.resize((target_width, target_height), Image.LANCZOS)

@app.post("/generate/horizontal")
async def generate_horizontal(file: UploadFile = File(...), text: str = Form(...)):
    img = Image.open(BytesIO(await file.read()))
    resized = resize_image(img, 1280, 720)

    output = BytesIO()
    resized.save(output, format="PNG")
    output.seek(0)

    return StreamingResponse(output, media_type="image/png")
