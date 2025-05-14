from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from PIL import Image
import smartcrop
import os

app = FastAPI()

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def smart_resize(image: Image.Image, width: int, height: int) -> Image.Image:
    cropper = smartcrop.SmartCrop()
    result = cropper.crop(image, width, height)
    box = (
        result['top_crop']['x'],
        result['top_crop']['y'],
        result['top_crop']['x'] + result['top_crop']['width'],
        result['top_crop']['y'] + result['top_crop']['height'],
    )
    cropped = image.crop(box)
    return cropped.resize((width, height), Image.LANCZOS)

@app.post("/render")
async def render_image(file: UploadFile = File(...)):
    input_image = Image.open(file.file).convert("RGB")

    sizes = {
        "horizontal": (1200, 675),
        "square": (1080, 1080),
        "vertical": (1080, 1350)
    }

    output_files = {}

    for name, (w, h) in sizes.items():
        resized = smart_resize(input_image, w, h)
        out_path = os.path.join(OUTPUT_DIR, f"{name}.jpg")
        resized.save(out_path, "JPEG")
        output_files[name] = out_path

    return {
        "horizontal": f"/download/horizontal",
        "square": f"/download/square",
        "vertical": f"/download/vertical"
    }

@app.get("/download/{size}")
async def download_image(size: str):
    path = os.path.join(OUTPUT_DIR, f"{size}.jpg")
    if not os.path.exists(path):
        return {"error": "File not found"}
    return FileResponse(path, media_type="image/jpeg", filename=f"{size}.jpg")
