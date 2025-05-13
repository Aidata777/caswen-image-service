from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io
import os

app = FastAPI()

@app.post("/generate/horizontal")
async def generate_horizontal(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Crea una nueva imagen horizontalmente más ancha, misma altura
        width, height = image.size
        new_width = int(height * 1.78)  # aprox 16:9
        new_image = Image.new("RGB", (new_width, height), color=(255, 255, 255))

        # Centra la imagen original dentro del nuevo lienzo horizontal
        offset = ((new_width - width) // 2, 0)
        new_image.paste(image, offset)

        # Guarda la nueva imagen en memoria
        output_buffer = io.BytesIO()
        new_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        # Devuelve la imagen como base64 en JSON (opcional)
        return JSONResponse(content={"message": "Imagen horizontal generada correctamente."})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Inicia uvicorn desde este script si no usas gunicorn
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("render_service:app", host="0.0.0.0", port=port, reload=False)

