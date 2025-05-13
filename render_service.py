from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from PIL import Image
from io import BytesIO
import os

app = FastAPI()

@app.post("/generate/horizontal")
async def generate_horizontal(file: UploadFile = File(...)):
    # Leer imagen de entrada
    contents = await file.read()
    image = Image.open(BytesIO(contents))

    # Redimensionar inteligentemente (a modo de ejemplo: 1200x628)
    target_size = (1200, 628)
    image = image.convert("RGB")
    image.thumbnail(target_size, Image.LANCZOS)

    # Crear nuevo fondo blanco y centrar la imagen redimensionada
    background = Image.new("RGB", target_size, (255, 255, 255))
    offset = ((target_size[0] - image.width) // 2, (target_size[1] - image.height) // 2)
    background.paste(image, offset)

    # Convertir a stream para respuesta HTTP
    img_byte_arr = BytesIO()
    background.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return StreamingResponse(img_byte_arr, media_type="image/png")
