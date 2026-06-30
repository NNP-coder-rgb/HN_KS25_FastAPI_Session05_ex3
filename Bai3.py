from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

students = [
    {"id": 1, "name": "Nguyen Van A"},
    {"id": 2, "name": "Tran Thi B"},
    {"id": 3, "name": "Le Van C"}
]

courses = [
    {"id": 1, "name": "FastAPI Basic", "capacity": 2},
    {"id": 2, "name": "Python OOP", "capacity": 2}
]

registrations = [
    {"id": 1, "student_id": 1, "course_id": 1},
    {"id": 2, "student_id": 2, "course_id": 1}
]

class CreateRegistration(BaseModel):
    student_id: int
    course_id: int

@app.post("/registrations", status_code=201)
def create_registration(new_registration: CreateRegistration):
    for re in registrations:
        if re["student_id"] == new_registration.student_id and re["course_id"] == new_registration.course_id:
            raise HTTPException(
                status_code=400,
                detail="Thong tin da ton tai"
            )
        
        new_registrations = {
            "id": len(registrations) + 1,
            "student_id": new_registration.student_id,
            "course_id": new_registration.course_id
        }

        registrations.append(new_registrations)
        return {
            "message": "Them thanh cong sinh vien",

        }
