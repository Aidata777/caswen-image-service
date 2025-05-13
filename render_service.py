from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
import io

app = FastAPI()

@app.post("/generate/horizontal")
async def generate_horizontal(file: UploadFile = File(...)):
    # Leer y abrir la imagen
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    
    # Redimensionar inteligentemente a horizontal (por ejemplo 1200x628)
    target_width, target_height = 1200, 628
    image = image.resize((target_width, target_height), Image.LANCZOS)
    
    # Preparar la respuesta como imagen PNG
    output = io.BytesIO()
    image.save(output, format="PNG")
    output.seek(0)

    return StreamingResponse(output, media_type="image/png")
