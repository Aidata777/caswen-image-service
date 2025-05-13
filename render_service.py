from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from PIL import Image
import io

app = FastAPI()

def resize_and_crop_to_horizontal(image: Image.Image) -> Image.Image:
    # Proporción horizontal estándar (16:9 por ejemplo)
    target_ratio = 16 / 9
    width, height = image.size
    current_ratio = width / height

    if current_ratio > target_ratio:
        # Imagen más ancha que deseado → recortar los lados
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        box = (left, 0, left + new_width, height)
    else:
        # Imagen más alta que deseado → recortar arriba y abajo
        new_height = int(width / target_ratio)
        top = (height - new_height) // 2
        box = (0, top, width, top + new_height)

    cropped = image.crop(box)
    return cropped

@app.post("/generate/horizontal")
async def generate_horizontal(file: UploadFile = File(...)):
    input_bytes = await file.read()
    image = Image.open(io.BytesIO(input_bytes)).convert("RGB")

    # Procesar la imagen
    output_image = resize_and_crop_to_horizontal(image)

    # Guardar en buffer y enviar como respuesta
    output = io.BytesIO()
    output_image.save(output, format="PNG")
    output.seek(0)
    return StreamingResponse(output, media_type="image/png")
