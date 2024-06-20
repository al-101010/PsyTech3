import random

from .hillclimber import Hillclimber
from code.classes.schedule import Schedule
from .fitted_start import FittedStart

class HeuristicsHillclimber(Hillclimber):
    
    def __init__(self, empty_schedule : Schedule):
        super().__init__(empty_schedule)
        self.random_start = FittedStart(empty_schedule)
        self.schedule = self.random_start.schedule

    def pick_activity(self, activities):
        activities = self.get_activities_with_most_maluspoints(activities, 10)
        return super().pick_activity(activities)

    def pick_student(self, students):
        students = self.get_students_with_most_maluspoints(students)
        return super().pick_student(students)
    
    def pick_students_to_switch(self, students, N):
        return self.get_students_with_most_maluspoints(students, N)
    
    def mutate_schedule(self, number_of_mutations: int = 1):
        for i in range(number_of_mutations):            
            if self.no_change_counter > 500 and self.schedule.archive:
                mutation = random.choices([self.switch_student_from_activities, self.switch_activities, self.split_activity], weights=(.4, .2, .4))[0]
            elif self.iteration < 1000:
                mutation = random.choices([self.switch_student_from_activities, self.switch_activities], weights=(.2, .8))[0]
            else:
                mutation = random.choices([self.switch_student_from_activities, self.switch_activities], weights=(.8, .2))[0]
            
            mutation()