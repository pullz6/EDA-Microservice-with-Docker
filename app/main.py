from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import io
from eda_processor import clean_columns, imbalance_checker  # Your functions
from typing import Optional

app = FastAPI(
    title="EDA Microservice",
    description="A reusable microservice for exploratory data analysis",
    version="0.1.0"
)


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Upload any file and get metadata (JSON response)"""
    content = await file.read()
    return JSONResponse({
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(content),
        "message": "File uploaded successfully"
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)