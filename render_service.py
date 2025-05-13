from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
from io import BytesIO

app = FastAPI()

@app.post("/generate/horizontal")
async def generate_horizontal(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(BytesIO(contents))

    # Redimensionado inteligente (manteniendo proporción, centrado)
    target_width = 1200
    target_height = 630
    image_ratio = image.width / image.height
    target_ratio = target_width / target_height

    if image_ratio > target_ratio:
        new_height = target_height
        new_width = int(image_ratio * new_height)
    else:
        new_width = target_width
        new_height = int(new_width / image_ratio)

    resized = image.resize((new_width, new_height), Image.LANCZOS)

    # Recortar al centro
    left = (resized.width - target_width) // 2
    top = (resized.height - target_height) // 2
    right = left + target_width
    bottom = top + target_height
    cropped = resized.crop((left, top, right, bottom))

    buf = BytesIO()
    cropped.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")

