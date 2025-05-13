from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from PIL import Image
import io
import os
import uuid

app = FastAPI()

@app.post("/generate/horizontal")
async def generate_horizontal(file: UploadFile = File(...)):
    # Leer la imagen recibida
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # Crear un lienzo horizontal (ejemplo: 1200x675)
    output_size = (1200, 675)
    canvas = Image.new("RGB", output_size, (255, 255, 255))

    # Redimensionar manteniendo la proporción
    image.thumbnail(output_size)

    # Centrar la imagen en el lienzo
    paste_position = (
        (output_size[0] - image.width) // 2,
        (output_size[1] - image.height) // 2
    )
    canvas.paste(image, paste_position)

    # Guardar imagen temporal
    filename = f"output_{uuid.uuid4()}.jpg"
    canvas.save(filename, "JPEG")

    # Devolver la imagen
    return FileResponse(filename, media_type="image/jpeg", filename=filename)
