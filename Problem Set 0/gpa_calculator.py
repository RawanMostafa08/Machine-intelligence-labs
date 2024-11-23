from typing import List
from college import Student, Course

def calculate_gpa(student: Student, courses: List[Course]) -> float:
    '''
    This function takes a student and a list of course
    It should compute the GPA for the student
    The GPA is the sum(hours of course * grade in course) / sum(hours of course)
    The grades come in the form: 'A+', 'A' and so on.
    But you can convert the grades to points using a static method in the course class
    To know how to use the Student and Course classes, see the file "college.py"  
    '''
    #TODO: ADD YOUR CODE HERE
    numerator = 0
    denominator = 0
    for course in courses:
        if course.grades.get(student.id,0) != 0:
            numerator += (course.hours * Course.convert_grade_to_points(course.grades[student.id]))
            denominator += course.hours

    if denominator==0:
        return 0
    return numerator/denominator