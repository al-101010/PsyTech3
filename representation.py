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




        
class Day:
    pass