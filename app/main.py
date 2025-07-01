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

@app.post("/analyze/")
async def analyze_data(
    file: UploadFile = File(...),
    target_col: Optional[str] = None,
    clean_data: bool = True
):
    """
    Process uploaded file and perform EDA.
    
    Parameters:
    - file: CSV file to analyze
    - target_col: Column name for imbalance analysis (optional)
    - clean_data: Whether to auto-clean columns (default True)
    """
    try:
        # Read the uploaded file
        contents = await file.read()
        
        # Try parsing as CSV
        try:
            df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error reading CSV: {str(e)}"
            )
        
        # Clean data if requested
        if clean_data:
            df = clean_columns(df)
        
        # Prepare response
        response = {
            "filename": file.filename,
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
        }
        
        # Add imbalance analysis if target column specified
        if target_col:
            if target_col not in df.columns:
                raise HTTPException(
                    status_code=400,
                    detail=f"Target column '{target_col}' not found in data"
                )
            imbalance = imbalance_checker(df, target_col)
            response["imbalance_analysis"] = imbalance
        
        return JSONResponse(content=response)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Processing error: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": app.version}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)