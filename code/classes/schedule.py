import math
import pandas as pd
import random
from .student import Student
from .course import Course
from .room import Room
from .activity import Activity


class Schedule:

    def __init__(self, students_data : str, courses_data : str, rooms_data : str) -> None:
        self.students = self.get_students_list(students_data)
        self.courses = self.get_courses_list(courses_data, self.students)
        self.rooms = self.get_rooms_list(rooms_data)
        self.activities = self.get_activities_list(self.courses)
        self.roomslots = self.get_room_slots()
        # TO DO: We still need to update some of these maluspoints
        self.room_maluspoints = 0
        self.student_maluspoints = 0
        self.overcapacity_maluspoints = 0
        self.total_maluspoints = 0

        self.add_students_courses(self.students, self.courses)


    def get_students_list(self, data : pd.DataFrame) -> list[Student]:
        """
        Iterate through students dataframe and create a Student class for each student.
        Returns a list of students in the form of Student classes.
        """
        data = pd.read_csv(data)

        # add students' full name and courses as column
        data['full_name'] = data['Voornaam'] + ' ' + data['Achternaam']
        data['courses'] = data[['Vak1', 'Vak2', 'Vak3', 'Vak4', 'Vak5']].values.tolist()

        students_list = []

        # loop over rows of dataframe and add Student class to list.
        for index, columns in data.iterrows():
            students_list.append(Student(columns['full_name'], columns['Stud.Nr.'], set(columns['courses'])))

        return students_list

    def get_courses_list(self, data : pd.DataFrame, all_students : list[Student]) -> list[Course]:
        """
        Iterate through courses dataframe and create a Course class for each Course.
        Returns a list of courses in the form of Course classes.
        """
        data = pd.read_csv(data)

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

    def get_rooms_list(self, data : pd.DataFrame) -> list[Room]:
        data = pd.read_csv(data)

        rooms_list = []
        for index, columns in data.iterrows():
            rooms_list.append(Room(columns['Zaalnummber'], columns['Max. capaciteit']))

        return rooms_list
    
    def get_activities_list(self, courses : list[Course]) -> list[Activity]:
        activities_list = []

        for course in courses:
            for activities in course.activities.values():
                for activity in activities:
                    activities_list.append(activity)

        return activities_list
    

    def get_room_slots(self):
        """Create archive of all possible roomslots"""
        # empty list for archive of all room-slots
        room_slots = []

        # add all room-slots to archive
        for room in self.rooms:
            for day in room.days:
                for time in room.timeslots:
                    room_slots.append((room, day, time))

        return room_slots


    def add_students_courses(self, students_list : list[Student], courses_list : list[Course]):
        """
        Add courses to students in the form of Subject classes.
        """
        for student in students_list:
            student.add_courses(courses_list)

    def get_evening_room_maluspoints(self):
        """ 
        Calculates malus points for using C0.110. 
        """

        evening_room_points = 0

        for room in self.rooms:
            if room.room_number == 'C0.110':
                for day, timeslots in room.schedule.items():
                    if timeslots.get('17') != 'Free':
                        evening_room_points += 5

        self.room_maluspoints = evening_room_points

        return self.room_maluspoints
    
    def get_overcapacity_maluspoints(self):
        """
        Get malus points for overcapacity (too many students in a room).
        """
        over_capacity_maluspoints = 0
        
        for activity in self.activities:
            if len(activity.students) > activity.room.capacity:
                over_capacity_maluspoints += (len(activity.students) - activity.room.capacity)
        
        return over_capacity_maluspoints

    def get_student_maluspoints(self):
        """
        Get total number of student related maluspoints (double bookings + free periods)
        """
        total_student_maluspoints = 0

        for student in self.students:
            total_student_maluspoints += student.get_total_maluspoints()
        
        return total_student_maluspoints
    
    def get_total_maluspoints(self):
        """
        Calculates total amount of malus points.
        """
        self.total_maluspoints = self.get_evening_room_maluspoints() + self.get_student_maluspoints() + self.get_overcapacity_maluspoints()

        return self.total_maluspoints