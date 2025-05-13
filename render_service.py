import os
import uvicorn
from fastapi import FastAPI, UploadFile, File
from PIL import Image
from io import BytesIO

app = FastAPI()

@app.post("/generate/horizontal")
async def generate_horizontal(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(BytesIO(contents))

    width, height = image.size
    new_width = int(width)
    new_height = int(width * 9 / 16)

    if new_height > height:
        new_height = height
        new_width = int(height * 16 / 9)

    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = left + new_width
    bottom = top + new_height

    cropped = image.crop((left, top, right, bottom))

    output = BytesIO()
    cropped.save(output, format="PNG")
    output.seek(0)

    return StreamingResponse(output, media_type="image/png")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("render_service:app", host="0.0.0.0", port=port, reload=False)
