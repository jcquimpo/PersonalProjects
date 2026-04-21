"""Main entry point for the FastAPI application."""

from app.main import app

if __name__ == "__main__":
    import uvicorn
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
