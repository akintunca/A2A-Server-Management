from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()


@router.get(
    "/",
    summary="Serve the index.html file",
    description="This endpoint serves the index.html file located in the static directory.",
    response_class=FileResponse,
    responses={
        200: {
            "description": "The index.html file was successfully served.",
            "content": {"text/html": {}},
        },
        404: {
            "description": "The index.html file was not found.",
            "content": {
                "application/json": {"example": {"detail": "index.html file not found"}}
            },
        },
    },
)
def root():
    """
    Root endpoint serving the index.html file.
    """
    index_file_path = os.path.join(
        os.path.dirname(__file__), "..", "static", "index.html"
    )

    if not os.path.exists(index_file_path):
        raise HTTPException(status_code=404, detail="index.html file not found")

    return FileResponse(index_file_path)
