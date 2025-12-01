import os
from fastapi import UploadFile

UPLOAD_DIR = "uploads"

def save_evidence(file: UploadFile, settlement_id: int):
    """
    Guarda una imagen localmente y retorna la ruta final.
    """
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    filename = f"settlement_{settlement_id}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return filepath
