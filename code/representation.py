import math
import pandas as pd

class Student:
    
    def __init__(self, name : str, number : str, course_names = set[str]) -> None:
        self.name = name
        self.student_number = number
        self.course_names = course_names
        self.courses = set()

    def add_courses(self, all_courses : set):
        """
        Add a student's courses to the set of courses as a course class.
        Also removes NA values.
        """
        for course in all_courses:
            if course.name in self.course_names:
                self.courses.add(course)


class Course:
    
    def __init__(self, name : str, students : list[Student]) -> None:
        self.name = name
        self.students = students
        self.activities = {}

    def add_activities(self, name : str, amount : int, capacity : int):
        if not 'h' in name:
            amount = math.ceil(len(self.students) / capacity)

        for i in range(1, amount + 1):
            name = f'{name}{i}'
            self.activities[name] = Activity(name, capacity)
        

class Activity:
    def __init__(self, name : str, capacity : str) -> None:
        self.name = name
        self.capacity = capacity

    def schedule(self, room, day, time):
        self.room = room
        self.day = day
        self.time = time

class Room:

    def __init__(self, room_number : str, capacity : str) -> None:
        self.room_number = room_number
        self.capacity = capacity

    def get_empty_schedule(self, days : list[str] = ['ma', 'di', 'wo', 'do', 'vr'], timeslots : list[str] = ['9', '11', '13', '15']):
        
        if self.room_number == 'C0.110':
            timeslots.append('17')

        self.schedule = {}

        for day in days:
            for timeslot in timeslots:
                self.schedule[day][timeslot] = 'Free'

   
class Day:
    pass

def get_students_list(data : pd.DataFrame) -> list[Student]:
    """
    Iterate through students dataframe and create a Student class for each student.
    Returns a list of students in the form of Student classes.
    """
    # add students' full name and subjects as column
    data['full_name'] = data['Voornaam'] + ' ' + data['Achternaam']
    data['subjects'] = data[['Vak1', 'Vak2', 'Vak3', 'Vak4', 'Vak5']].values.tolist()   
    
    students_list = []

    # loop over rows of dataframe and add Student class to list.
    for index, columns in data.iterrows():
        students_list.append(Student(columns['full_name'], columns['Stud.Nr.'], set(columns['subjects'])))

    return students_list


# read students and subjects as dataframe
students = pd.read_csv('../data/studenten_en_vakken.csv')
subjects = pd.read_csv('../data/vakken.csv')
rooms = pd.read_csv('../data/zalen.csv')
