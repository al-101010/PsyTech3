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
    
    def __init__(self, name : str, students : list[Student], activity_amounts : dict) -> None:
        self.name = name
        self.students = students
        self.activity_amounts = activity_amounts
        self.activities = {}

        self.add_activities(activity_amounts)



    def add_activities(self, activity_amounts : dict):
        for activity_name, (amount, capacity) in activity_amounts.items():
            if amount == 0:
                continue

            if not 'h' in activity_name:
                amount = math.ceil(len(self.students) / capacity)
        
            for i in range(1, amount + 1):
                name = f'{activity_name}{i}'
                self.activities[name] = Activity(name, capacity)


class Activity:
    def __init__(self, name : str, capacity : str) -> None:
        self.name = name
        self.capacity = capacity
        self.scheduled = False

    def schedule(self, room, day, time):
        self.room = room
        self.day = day
        self.time = time
        self.scheduled = True

class Room:

    def __init__(self, room_number : str, capacity : str) -> None:
        self.room_number = room_number
        self.capacity = capacity

        self.get_empty_schedule()

    def get_empty_schedule(self, days : list[str] = ['ma', 'di', 'wo', 'do', 'vr'], timeslots : list[str] = ['9', '11', '13', '15']):
        
        if self.room_number == 'C0.110':
            timeslots.append('17')
        else:
            timeslots = ['9', '11', '13', '15']

        self.schedule = {}

        for day in days:
            self.schedule[day] = {}
            for timeslot in timeslots:
                self.schedule[day][timeslot] = 'Free'

   
class Day:
    pass

def get_students_list(data : pd.DataFrame) -> list[Student]:
    """
    Iterate through students dataframe and create a Student class for each student.
    Returns a list of students in the form of Student classes.
    """
    # add students' full name and courses as column
    data['full_name'] = data['Voornaam'] + ' ' + data['Achternaam']
    data['courses'] = data[['Vak1', 'Vak2', 'Vak3', 'Vak4', 'Vak5']].values.tolist()   
    
    students_list = []

    # loop over rows of dataframe and add Student class to list.
    for index, columns in data.iterrows():
        students_list.append(Student(columns['full_name'], columns['Stud.Nr.'], set(columns['courses'])))

    return students_list

def get_courses_list(data : pd.DataFrame, all_students : list[Student]) -> list[Course]:
    """
    Iterate through courses dataframe and create a Course class for each Course.
    Returns a list of courses in the form of Course classes.
    """
    courses_list = []

    # loop over rows of dataframe (courses)
    for index, columns in data.iterrows():
    
        course_students = []

        # loop over all students in any course
        for student in all_students:
            
            # add student to this course list if they follow the course
            if columns['Vak'] in student.course_names:
                course_students.append(student)

        lectures = (columns['#Hoorcolleges'], math.inf)
        tutorials = (columns['#Werkcolleges'], columns['Max. stud. Werkcollege'])
        practicals = (columns['#Practica'], columns['Max. stud. Practicum'])

        activity_amounts = {'h' : lectures, 'w' : tutorials, 'p' : practicals}

        # add course to courses list
        courses_list.append(Course(columns['Vak'], course_students, activity_amounts))

    return courses_list

def get_rooms_list(data : pd.DataFrame) -> list[Room]:
    rooms_list = []
    for index, columns in data.iterrows():
        rooms_list.append(Room(columns['Zaalnummber'], columns['Max. capaciteit']))

    return rooms_list

def add_students_subjects(students_list : list[Student], courses_list : list[Course]):
    """
    Add courses to students in the form of Subject classes.
    """
    for student in students_list:
        student.add_courses(courses_list)

def schedule_courses(courses : list[Course], rooms : list[Room]):
    for course in courses:
        for activity_instance in course.activities.values():
                for room in rooms:
                    for day, timeslots in room.schedule.items():
                        for timeslot, availability in timeslots.items():
                            while activity_instance.scheduled == False:
                                if availability == 'Free':
                                    room.schedule[day][timeslot] = 'Occupied'
                                    activity_instance.schedule(room, day, timeslot)
                                else:
                                    break
        

def get_output(students : list[Student]):
    rows = []

    for student in students:
        for course in student.courses:
            for activity_instance in course.activities.values():
                rows.append([student.name, course.name, activity_instance.name, activity_instance.room.room_number, activity_instance.day, activity_instance.time])

        
    # create dataframe of schedule
    schedule = pd.DataFrame(rows, columns=['Student', 'Vak', 'Activiteit', 'Zaal', 'Dag', 'Tijdslot'])

    schedule.to_csv('../data/test_output.csv', index=False)

    return schedule


# read students and courses as dataframe
students = pd.read_csv('../data/studenten_en_vakken.csv')
courses = pd.read_csv('../data/vakken.csv')
rooms = pd.read_csv('../data/zalen.csv')

students_list = get_students_list(students)
courses_list = get_courses_list(courses, students_list)
rooms_list = get_rooms_list(rooms)
add_students_subjects(students_list, courses_list)

schedule_courses(courses_list, rooms_list)
print(get_output(students_list))

