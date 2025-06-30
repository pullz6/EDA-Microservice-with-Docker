from fastapi import FastAPI

app = FastAPI(title="EDA Microservice",
              description="A reusable microservice for exploratory data analysis")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allows ALL domains to access your API
    allow_methods=["*"],          # Allows ALL HTTP methods (GET, POST, etc.)
    allow_headers=["*"],          # Allows ALL headers in requests
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Critical: Use 0.0.0.0, not 127.0.0.1