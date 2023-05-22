from typing import List

from fastapi import APIRouter
from fastapi import  status
from fastapi import  Depends
from fastapi import  HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.course_model import CourseModel
from schemas.course_schema import CourseSchema
from core.deps import get_session

router = APIRouter()

#POST course 
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CourseSchema)
async def post_course(course: CourseSchema, db: AsyncSession = Depends(get_session)):
    new_course = CourseModel(title=course.title,lessons=course.lessons, hours=course.hours)

    db.add(new_course)
    await db.commit()

    return new_course

#GET Courses
@router.get('/', response_model=List[CourseSchema])
async def get_courses(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel)
        result = await session.execute(query)
        courses: List[CourseModel] = result.scalars().all()

        return courses
    
#GET Course 
@router.get('/{course_id}', response_model=CourseSchema, status_code=status.HTTP_200_OK)
async def get_course(course_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == course_id)
        result = await session.execute(query)
        course = result.scalar_one_or_none()

        if course:
            return course
        else:
            raise HTTPException(detail='Course not found!', status_code=status.HTTP_404_NOT_FOUND)

#PUT Course
@router.put('/{course_id}', response_model=CourseSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_course(course_id: int, course: CourseSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == course_id)
        result = await session.execute(query)
        course_up = result.scalar_one_or_none()

        if course_up:
            course_up.title = course.title
            course_up.lessons = course.lessons
            course_up.hours = course.hours

            await session.commit()

            return course_up
        else:
            raise HTTPException(detail='Course not found!', status_code=status.HTTP_404_NOT_FOUND)
        
#Delete Course
@router.delete('/{course_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == course_id)
        result = await session.execute(query)
        course_del = result.scalar_one_or_none()

        if course_del:
            await session.delete(course_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Course not found!', status_code=status.HTTP_404_NOT_FOUND)