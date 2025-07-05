from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
import pandas as pd
import io
import numpy as np
from eda_processor import clean_columns, imbalance_checker  # Your custom functions

app = FastAPI(
    title="EDA Microservice",
    description="A reusable microservice for exploratory data analysis",
    version="0.1.0"
)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Endpoint for uploading and processing CSV files"""
    try:
        # 1. Read and validate the file
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")

        # 2. Process the file content
        contents = await file.read()
        
        try:
            # Try reading with default UTF-8 encoding first
            df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        except UnicodeDecodeError:
            # Fallback to other encodings if UTF-8 fails
            try:
                df = pd.read_csv(io.StringIO(contents.decode('latin-1')))
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to decode file: {str(e)}")
        except pd.errors.EmptyDataError:
            raise HTTPException(status_code=400, detail="The file is empty")
        except pd.errors.ParserError:
            raise HTTPException(status_code=400, detail="Invalid CSV format")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading CSV: {str(e)}")

        # 3. Basic validation
        if df.empty:
            raise HTTPException(status_code=400, detail="The file contains no data")

        # 4. Process the data
        try:
            cleaned_df, dt_cols, num_cols = clean_columns(df)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Data cleaning failed: {str(e)}")

        # 5. Generate response
        response = {
            "filename": file.filename,
            "original_columns": list(df.columns),
            "cleaned_columns": list(cleaned_df.columns),
            "converted_datetime_cols": dt_cols,
            "converted_numeric_cols": num_cols,
            "shape": cleaned_df.shape,
            "sample_data": cleaned_df.head().to_dict(orient="records")
        }

        # 6. Return CSV file for download
        csv_data = cleaned_df.to_csv(index=False)
        return StreamingResponse(
            io.StringIO(csv_data),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=processed_{file.filename}"
            }
        )

    except HTTPException:
        raise  # Re-raise our custom HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        await file.close()

@app.post("/test/")
async def test_endpoint():
    """Test endpoint with generated data"""
    try:
        # Create test data
        test_data = {
            'date': pd.date_range(start='2023-01-01', periods=5),
            'value': np.random.randint(1, 100, 5),
            'category': ['A', 'B', 'A', 'C', 'B']
        }
        df = pd.DataFrame(test_data)
        
        # Process the test data
        cleaned_df, dt_cols, num_cols = clean_columns(df)
        imbalance = imbalance_checker(cleaned_df, 'category')
        
        return JSONResponse({
            "status": "success",
            "test_data": df.to_dict(orient="records"),
            "cleaning_results": {
                "datetime_columns": dt_cols,
                "numeric_columns": num_cols
            },
            "imbalance_analysis": imbalance
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)