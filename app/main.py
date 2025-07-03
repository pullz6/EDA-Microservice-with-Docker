#Fastapi libraries to be used
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse

#Customer functions as well as required utility libraries
from eda_processor import clean_columns, imbalance_checker
import pandas as pd
import numpy as np 

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


@app.post("/test/")
async def test_eda():
    """Testing data and the eda"""
    df = pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))
    
    # Initialize response
    response = {
        "test_data_sample": df.head().to_dict(orient="records"),
        "cleaning": {},
        "imbalance_analysis": {}
    }
    
    try: 
        cleaned_df,cols_dt,cols_int = clean_columns(df)
        response["cleaning"] = {
            "status": "success",
            "dtypes_after_cleaning": str(cleaned_df.dtypes.to_dict())
        }
    except Exception as e:
        response["cleaning"] = {
            "status": "failed",
            "error": str(e)
        }
    
    try: 
        imbalance_result = imbalance_checker(df, 'A')
        response["imbalance_analysis"] = {
            "status": "success",
            "result": imbalance_result
        }
    except Exception as e:
        response["imbalance_analysis"] = {
            "status": "failed",
            "error": str(e)
        }
        
    folder_path = r"C:\Users\HP\Desktop\excel files"
    file_location = f'{folder_path}{os.sep}{file_name}.xlsx'#os.sep is used to seperate with a \
    return FileResponse(file_location, media_type='application/octet-stream', filename=file_name)
    
    return JSONResponse(content=response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)