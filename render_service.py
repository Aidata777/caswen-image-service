from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from PIL import Image
from io import BytesIO

app = FastAPI()

def smart_crop(image: Image.Image, target_width: int, target_height: int) -> Image.Image:
    img_width, img_height = image.size
    target_ratio = target_width / target_height
    img_ratio = img_width / img_height

    # Decide crop strategy
    if img_ratio > target_ratio:
        # Crop width
        new_width = int(target_ratio * img_height)
        offset = (img_width - new_width) // 2
        cropped = image.crop((offset, 0, offset + new_width, img_height))
    else:
        # Crop height
        new_height = int(img_width / target_ratio)
        offset = (img_height - new_height) // 2
        cropped = image.crop((0, offset, img_width, offset + new_height))

    return cropped.resize((target_width, target_height), Image.LANCZOS)

@app.post("/generate/horizontal")
async def generate_horizontal(file: UploadFile = File(...), text: str = Form(...)):
    img = Image.open(BytesIO(await file.read()))
    resized = smart_crop(img, 1280, 720)

    output = BytesIO()
    resized.save(output, format="PNG")
    output.seek(0)
    return StreamingResponse(output, media_type="image/png")
