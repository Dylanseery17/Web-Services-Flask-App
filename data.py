student_data = {}

def setup():
    from schema import  Student

    global student_data

    student1 = Student(
        id="1",
        name="Dylan Seery",
        gpa="3.60",
    )

    student_data = {"1": student1}

def get_student(id):
    return student_data.get(id)