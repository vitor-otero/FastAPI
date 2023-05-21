from fastapi import FastAPI

from core.configs import settings
from api.v1.api import api_router

app = FastAPI(title='Courses API - FastAPI SQL Alchemy')
app.include_router(api_router, prefix=settings.API_V1_STR)

# /api/v1/courses
# /api/v1/users 


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level='info')