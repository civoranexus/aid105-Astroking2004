from fastapi import FastAPI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Test API")

@app.get("/health")
def health():
    logger.info("Health check called")
    return {"status": "ok"}

@app.get("/test")
def test():
    logger.info("Test called")
    return {"message": "test"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
