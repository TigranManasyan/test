class StudentView:
    def display_student_list(self, students: list[Student]):
        print("====Student list====")
        if not students:
            print("Empty List")
            return

        for student in students:
            print(f"ID: {student.id} | Name: {student.name}")

    def display_student_details(self, student: Student | None):
        print("====Student details====")
        if student:
            print(f"ID: {student.id} | Name: {student.name} | Grade: {student.grade}")
        else:
            print("Student not found")

    def display_message(self, message: str):
        print(f"{message}")