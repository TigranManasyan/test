from dataclasses import dataclass

@dataclass
class Student:
    id: int
    name: str
    grade: float

class StudentModel:
    def __init__(self):
        self._students = [
            Student(1, "Aram", 18.5),
            Student(2, "Hayk", 18.9),
            Student(3, "Arsen", 20)
        ]
    def get_all_students(self) -> list[Student]:
        return self._students

    def add_student(self, name: str, grade: float) -> Student:
        new_id = len(self._students) + 1 if self._students else 1
        student = Student(new_id, name, grade)
        self._students.append(student)
        return student

    def get_student_by_id(self, student_id: int) -> Student | None:
        for student in self._students:
            if student_id == student.id:
                return student
        return None