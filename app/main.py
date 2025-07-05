from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import StreamingResponse, JSONResponse
import pandas as pd
import io
import numpy as np
from typing import Optional
from .eda_processor import clean_columns, imbalance_checker

app = FastAPI(
    title="EDA Microservice",
    description="A reusable microservice for exploratory data analysis",
    version="0.1.0"
)

@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    target_column: Optional[str] = Query(None, description="Column name for imbalance analysis")
):
    """Endpoint for uploading and processing CSV files"""
    try:
        # 1. Read and validate the file
        if not file.filename.endswith(('.csv', '.xlsx')):
            raise HTTPException(status_code=400, detail="Only CSV or Excel files are supported")

        # 2. Process the file content
        contents = await file.read()
        
        try:
            if file.filename.endswith('.csv'):
                # Try reading with default UTF-8 encoding first
                df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
            else:  # Excel file
                df = pd.read_excel(io.BytesIO(contents))
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(io.StringIO(contents.decode('latin-1')))
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to decode file: {str(e)}")
        except pd.errors.EmptyDataError:
            raise HTTPException(status_code=400, detail="The file is empty")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

        # 3. Basic validation
        if df.empty:
            raise HTTPException(status_code=400, detail="The file contains no data")

        # 4. Process the data
        try:
            cleaned_df, dt_cols, num_cols = clean_columns(df)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Data cleaning failed: {str(e)}")

        # 5. Imbalance analysis (if target column specified)
        imbalance_result = None
        if target_column:
            if target_column not in cleaned_df.columns:
                available_cols = list(cleaned_df.columns)
                raise HTTPException(
                    status_code=400,
                    detail=f"Target column '{target_column}' not found. Available columns: {available_cols}"
                )
            try:
                imbalance_result = imbalance_checker(cleaned_df, target_column)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Imbalance analysis failed: {str(e)}")

        # 6. Generate response
        response = {
            "filename": file.filename,
            "original_columns": list(df.columns),
            "cleaned_columns": list(cleaned_df.columns),
            "converted_datetime_cols": dt_cols,
            "converted_numeric_cols": num_cols,
            "shape": cleaned_df.shape,
            "sample_data": cleaned_df.head().to_dict(orient="records"),
            "target_column_used": target_column,
            "imbalance_analysis": imbalance_result
        }

        # 7. Return CSV file for download
        csv_data = cleaned_df.to_csv(index=False)
        return StreamingResponse(
            io.StringIO(csv_data),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=processed_{file.filename}"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        await file.close()

@app.post("/test/")
async def test_endpoint(
    target_column: Optional[str] = Query(None, description="Column name for imbalance analysis")
):
    """Test endpoint with generated data"""
    try:
        # Create test data
        test_data = {
            'date': pd.date_range(start='2023-01-01', periods=5),
            'value': np.random.randint(1, 100, 5),
            'category': ['A', 'B', 'A', 'C', 'B'],
            'status': ['active', 'inactive', 'active', 'active', 'pending']
        }
        df = pd.DataFrame(test_data)
        
        # Process the test data
        cleaned_df, dt_cols, num_cols = clean_columns(df)
        
        # Imbalance analysis (if target column specified)
        imbalance_result = None
        if target_column:
            if target_column not in cleaned_df.columns:
                available_cols = list(cleaned_df.columns)
                return JSONResponse(
                    status_code=400,
                    content={"error": f"Target column '{target_column}' not found", 
                            "available_columns": available_cols}
                )
            imbalance_result = imbalance_checker(cleaned_df, target_column)
        
        return JSONResponse({
            "status": "success",
            "test_data": df.to_dict(orient="records"),
            "cleaning_results": {
                "datetime_columns": dt_cols,
                "numeric_columns": num_cols
            },
            "target_column_used": target_column,
            "imbalance_analysis": imbalance_result
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)