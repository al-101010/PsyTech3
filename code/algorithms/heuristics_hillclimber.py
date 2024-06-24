import random
import math

from .hillclimber import Hillclimber
from code.classes.schedule import Schedule
from .fitted_start import FittedStart

class HeuristicsHillclimber(Hillclimber):
    
    def __init__(self, empty_schedule : Schedule):
        super().__init__(empty_schedule)
        self.fitted_start = FittedStart(empty_schedule)
        self.schedule = self.fitted_start.schedule

    def get_activities_with_most_maluspoints(self, activities, top_n: int=40) -> list:
        return sorted(activities, key=lambda activity: activity.maluspoints, reverse=True)[:top_n]
    
    def get_students_with_most_maluspoints(self, students, top_n: int=20) -> list:
        return sorted(students, key=lambda student: student.maluspoints, reverse=True)[:top_n]


    def pick_student(self, students):
        N = math.ceil(len(students) / 3)
        top_students = self.get_students_with_most_maluspoints(students, N)
        return super().pick_student(top_students)
    
    def pick_students_to_switch(self, students, N):
        return self.get_students_with_most_maluspoints(students, N)
    
    def mutate_schedule(self, number_of_mutations: int = 1):
        for i in range(number_of_mutations):            
            if self.no_change_counter > 500 and self.schedule.archive:
                mutation = random.choices([self.switch_student_from_activities, self.switch_activities, self.split_activity], weights=(.2, .2, .6))[0]
            elif self.iteration < 1000:
                mutation = random.choices([self.switch_student_from_activities, self.switch_activities], weights=(.2, .8))[0]
            else:
                mutation = random.choices([self.switch_student_from_activities, self.switch_activities], weights=(.8, .2))[0]
            
            mutation()

        # if self.no_change_counter > 500 and self.schedule.archive:
        #     mutation = random.choice([self.switch_student_from_activities, self.switch_activities, self.split_activity])
        # else:
        #     mutation = random.choice([self.switch_student_from_activities, self.switch_activities])
        # mutation()

    
class ProblematicActivityClimber(HeuristicsHillclimber):
    
    def pick_activity(self, activities):
        N = math.ceil(len(activities) / 3)
        top_activities = self.get_activities_with_most_maluspoints(activities, N)
        return super().pick_activity(top_activities)