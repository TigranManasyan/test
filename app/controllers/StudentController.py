class StudentController:
    def __init__(self, model: StudentModel, view: StudentView):
        self.model = model
        self.view = view

    def show_all_students(self):
        students = self.model.get_all_students()
        self.view.display_student_list(students)

    def add_new_student(self, name, grade):
        student = self.add_student(name, grade)
        self.view.display_message(f"Student created: {student}")
        self.show_all_students()

    def show_student_details(self, student_id):
        student = self.model.get_student_by_id(student_id)
        self.view.display_student_details(student)