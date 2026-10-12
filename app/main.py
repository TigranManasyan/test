from controllers.StudentController import StudentController
from models.StudentModel import StudentModel
from views.StudentView import StudentView

if __name__ == '__main__':
    model = StudentModel()
    view = StudentView()
    controller = StudentController(model, view)

    controller.show_all_students()