from fastapi import APIRouter

router = APIRouter()

@router.get('/api/v1/users')
async def get_courses():
    return {"info": "All users"}