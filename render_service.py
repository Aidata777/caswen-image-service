from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
import io
import os

app = FastAPI()

@app.post("/generate/horizontal")
async def generate_horizontal(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    # Resize a formato horizontal (ej. 1200x628)
    target_width, target_height = 1200, 628
    image = image.resize((target_width, target_height), Image.LANCZOS)

    output = io.BytesIO()
    image.save(output, format="PNG")
    output.seek(0)

    return StreamingResponse(output, media_type="image/png")


# Esto es solo para que Render detecte el puerto correctamente si usaras uvicorn/gunicorn directamente
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("render_service:app", host="0.0.0.0", port=port, reload=True)
