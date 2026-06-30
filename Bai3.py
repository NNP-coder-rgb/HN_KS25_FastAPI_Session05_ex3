# Input: JSON gồm student_id (int) và course_id (int).
# Output thành công (201 Created): JSON object chứa thông tin đăng ký mới kèm id.
# Output thất bại:
# Lỗi 404: Không tìm thấy student_id hoặc course_id.
# Lỗi 400: Đăng ký trùng hoặc khóa học hết chỗ (capacity).
# 2. Đề xuất giải pháp
# Quy trình xử lý tuần tự gồm 5 bước:
# Check Student: Dùng next() tìm student_id. 
# Không thấy Lỗi 404.
# Check Course: Dùng next() tìm course_id và lấy capacity. 
# Không thấy Lỗi 404.
# Check Trùng (Bẫy 1): Chạy for quét danh sách. 
# Trùng cả student_id và course_id Lỗi 400.
# Check Sĩ số (Bẫy 2): Chạy for đếm số người đã đăng ký khóa học. 
# Nếu Lỗi 400.
# Lưu dữ liệu: Tạo id mới (len + 1), chèn vào danh sách và 
# return object vừa tạo.

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

class RegistrationResponse(BaseModel):
    id: int
    student_id: int
    course_id: int

@app.post("/registrations", status_code=201)
def create_registration(new_registration: CreateRegistration):

    student = next((s for s in students if s["id"] == new_registration.student_id), None)
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    
    course = next((c for c in courses if c["id"] == new_registration.course_id), None)
    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )


    for re in registrations:
        if re["student_id"] == new_registration.student_id and re["course_id"] == new_registration.course_id:
            raise HTTPException(
                status_code=400,
                detail="Student already registered this course"
            )
    count = 0
    for r in registrations:
        if r["course_id"] == new_registration.course_id:
            count += 1

    if count >= course["capacity"]:
        raise HTTPException(
            status_code=400,
            detail="Course is full"
        )
        
    new_registrations = {
        "id": len(registrations) + 1,
        "student_id": new_registration.student_id,
        "course_id": new_registration.course_id
    }

    registrations.append(new_registrations)
    return {
        "message": "Them thanh cong sinh vien",
        "data": new_registrations

    }
