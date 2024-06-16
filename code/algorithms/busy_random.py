from .random_alg import Random
from functools import reduce
import random 
import copy 

class BusyRandom(Random):
    """ 
    Inherits from Random schedule. Difference: Activities are selected on a busy-comes-first 
    basis and not randomly. 

    TODOs: 
    - test more 
    
     """
    
    # TODO: remove random seed comments
    
    # random.seed(1)

    def __init__(self, empty_schedule) -> None:
        super().__init__(empty_schedule)
        
        self.archive = copy.copy(self.schedule.roomslots)
        self.sort_courses_by_busy()
        self.schedule_courses(self.archive)


    def get_busy_index(self):
        """ Adds busy indices to all courses"""
        
        # loop over courses
        for course in self.schedule.courses:

            busy_index = 0 
            
            # get number activities in course: int
            total_course_activities = len(reduce(lambda a, b: a+b, course.activities.values()))
            
            # get number students enrolled in course: int  
            course_students = len(course.students)
 
            # get number courses of each enrolled student: int 
            total_student_courses = self.get_total_student_courses(course.students)

            # sum all up to index  
            busy_index += total_course_activities + course_students + total_student_courses
            
            # add busy index label to course 
            course.busy_index = busy_index

    
    def get_total_student_courses(self, course_students):
        """ Gets number of courses of each student enrolled in course"""
        
        student_courses = 0
        
        for student in course_students:
                student_courses += len(student.courses)
        
        return student_courses
        
        
    def sort_courses_by_busy(self):
        """ Sorts courses by index of busyness, busiest first."""
        
        self.get_busy_index()

        sorted_courses = sorted(self.schedule.courses, key=lambda course:course.busy_index, reverse=True)
        
        self.schedule.courses = sorted_courses


    def schedule_courses(self, archive):
        """
        Schedule sorted activities on a random roomslot that is available.
        """
        
        # schedule activities according to sorted courses 
        self.schedule.activities = self.schedule.get_activities_list(self.schedule.courses)

        # loop over all activities
        for activity in self.schedule.activities:  
           roomslot = self.pick_random_roomslot(archive)
           self.schedule_activity(activity, roomslot, archive)



