from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import shutil
from typing import List

app = FastAPI()

# Directory to store images
IMAGE_DIR = "images"

# Create the directory if it doesn't exist
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(IMAGE_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}

@app.get("/images/{filename}")
async def get_image(filename: str):
    file_path = os.path.join(IMAGE_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="Image not found")

@app.delete("/images/{filename}")
async def delete_image(filename: str):
    file_path = os.path.join(IMAGE_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"detail": "Image deleted"}
    else:
        raise HTTPException(status_code=404, detail="Image not found")

@app.get("/images/")
async def list_images():
    files = os.listdir(IMAGE_DIR)
    return {"images": files}
