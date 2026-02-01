from fastapi import APIRouter, status


router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def api_status():
    """API Status Check"""
    return {"Message": "Automation API running!"}
