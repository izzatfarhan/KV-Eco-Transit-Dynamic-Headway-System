from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import logging

# Import routers
from src.trains import router as trains_router

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Klang Valley Eco-Transit Optimizer",
    description="Dynamic Headway System API for Malaysian transit network",
    version="1.0.0"
)

# Centralized Error Handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Catch standard HTTPExceptions and return a unified error response.
    """
    logger.error(f"HTTP Exception: {exc.detail} on route {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "error": True},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Catch any unhandled exceptions to prevent server crashes and return 500.
    """
    logger.error(f"Unhandled Exception: {str(exc)} on route {request.url.path}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "error": True},
    )

app.include_router(trains_router.router, prefix="/api/v1/trains", tags=["Trains"])

@app.get("/health")
async def health_check():
    """
    Basic health check endpoint for monitoring uptime.
    """
    return {"status": "ok"}
