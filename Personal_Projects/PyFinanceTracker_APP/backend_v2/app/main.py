"""FastAPI Stock Dashboard Backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.routes import stocks

# Initialize FastAPI app
app = FastAPI(
    title="Stock Dashboard API",
    description="Real-time stock tracking and analysis API",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(stocks.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Stock Dashboard Backend v2.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


# Mount static files for React SPA if they exist
# This will serve the React build files
static_files_path = os.path.join(os.path.dirname(__file__), "..", "frontend_build")
if os.path.exists(static_files_path):
    app.mount("/", StaticFiles(directory=static_files_path, html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
