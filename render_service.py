from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os
import uvicorn

app = FastAPI()

SIZES = {
    "vertical": (1080, 1350),
    "cuadrado": (1080, 1080),
    "horizontal": (1200, 628)
}

def procesar_imagen(img: Image.Image, texto: str, size: tuple) -> Image.Image:
    img = img.convert("RGBA").resize(size, Image.LANCZOS)
    width, height = img.size

    grad = Image.new('L', (1, height), color=0xFF)
    for y in range(height):
        opacity = int(255 * max(0, 1 - y / (height * 0.4)))
        grad.putpixel((0, y), opacity)
    grad = grad.resize((width, height))
    grad_rgba = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    grad_rgba.putalpha(grad)

    final = Image.alpha_composite(img, grad_rgba)

    draw = ImageDraw.Draw(final)
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()

    # ✅ Usar textbbox en lugar de textsize
    bbox = draw.textbbox((0, 0), texto, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (width - text_w) / 2
    y = height - text_h - 80

    draw.text((x, y), texto, font=font, fill=(255, 255, 255, 255))
    return final

@app.post("/generate")
async def generate(file: UploadFile = File(...), texto: str = Form(...)):
    raw = await file.read()
    original = Image.open(io.BytesIO(raw))

    result = {}
    for nombre, size in SIZES.items():
        editada = procesar_imagen(original, texto, size)
        buffer = io.BytesIO()
        editada.save(buffer, format="PNG")
        buffer.seek(0)
        result[nombre] = base64.b64encode(buffer.read()).decode("utf-8")

    return JSONResponse(content=result)

# 🔧 Para correr en Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("render_service:app", host="0.0.0.0", port=port)

