from typing import List, Dict, Optional, Any

from fastapi.responses import JSONResponse
from fastapi import Depends, Response
from fastapi import Path
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status

from time import sleep

from models import Course
from models import courses

def fake_db():
    try:
        print('Opening database...')
        sleep(1)
    finally:
        print('Closing database...')
        sleep(1)

app = FastAPI(title='v0t.org API',
              version='0.0.1',
              description='One api for tests',
              )


@app.get('/courses/',
         description='Return all courses or empty list of courses',
         summary='Return all courses',
         response_model=List[Course],
         response_description='Courses fund successfuly')
async def get_courses(db: Any = Depends(fake_db)):
    return courses


@app.get('/courses/{course_id}')
async def get_course(course_id: int = Path(title='Course ID', description='Must to be between 1 and 2', gt=0, lt=3), db: Any = Depends(fake_db)):
    try:
        course = courses[course_id]
        return course
    except KeyError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Course not found")

@app.post('/courses/', status_code=status.HTTP_201_CREATED, response_model=Course)
async def create_course(course: Course):
    next_id: int = len(courses) + 1
    course.id = next_id
    courses.append(course)
    
    return course


@app.put('/courses/{course_id}')
async def put_course(course_id: int, course: Course, db: Any = Depends(fake_db)):
    if course_id in courses:
        courses[course_id] = course
        del course.id

        return  course
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The ID {course_id} not exist')   
    
@app.delete('/courses/{course_id}')
async def delete_course(course_id: int, db: Any = Depends(fake_db)):
    if course_id in courses:
        del courses[course_id]
        # return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The ID {course_id} not exist')   
    

@app.get('/calculator')
async def calculate(a:int ,b: int,c: Optional[int] = None):
    plus: int = a + b
    if c: 
        plus = plus + c 
    
    return {"result": plus}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)