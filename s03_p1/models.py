from typing import Optional
from pydantic import BaseModel, validator

class Course(BaseModel):
    id: Optional[int] = None
    title: str
    lessons: str
    hours: int

    @validator('title')
    def validate_title(cls, value):
        words = value.split(' ')
        #Validate 1
        if len(words) <3:
            raise ValueError('The title must be at least 3 words')
        #Validate 2
        if value.islower():
            raise ValueError('The title must be in capital letters')
        
        return value

courses = [
    Course(id=1, title='Programing for newbies', lessons=112, hours=58),
    Course(id=2, title='Programming for hackers', lessons=87, hours=67)
]
