import random
import math
import copy

from .hillclimber import Hillclimber
from code.classes.schedule import Schedule

class HeuristicsHillclimber(Hillclimber):
    def get_activities_with_most_maluspoints(self, activities, top_n: int=40) -> list:
        return sorted(activities, key=lambda activity: activity.maluspoints, reverse=True)[:top_n]
    
    def get_students_with_most_maluspoints(self, students, top_n: int=20) -> list:
        return sorted(students, key=lambda student: student.maluspoints, reverse=True)[:top_n]

    
class ProblematicActivityClimber(HeuristicsHillclimber):
    
    def pick_activity(self, activities):
        N = math.ceil(len(activities) / 3)
        top_activities = self.get_activities_with_most_maluspoints(activities, N)
        return super().pick_activity(top_activities)
    
class ProblematicStudentsClimber(HeuristicsHillclimber):
    
    def pick_student(self, students):
        N = math.ceil(len(students) / 3)
        top_students = self.get_students_with_most_maluspoints(students, N)
        return super().pick_student(top_students)
    
    def pick_students_to_switch(self, students, N):
        return self.get_students_with_most_maluspoints(students, N)
    
class MutationProbabilityClimber(HeuristicsHillclimber):
    def mutate_schedule(self, number_of_mutations: int = 1):
        for i in range(number_of_mutations):            
            if self.no_change_counter > 500 and self.schedule.archive:
                mutation = random.choices([self.switch_student_from_activities, self.switch_activities, self.add_activity_to_course], weights=(.2, .2, .6))[0]
            elif self.iteration < 1000:
                mutation = random.choices([self.switch_student_from_activities, self.switch_activities], weights=(.2, .8))[0]
            else:
                mutation = random.choices([self.switch_student_from_activities, self.switch_activities], weights=(.8, .2))[0]
            
            mutation()

class IncreasingMutationsClimber(HeuristicsHillclimber):
    def pick_number_mutations(self):
        if self.no_change_counter > 1800:
            return 10
        elif self.no_change_counter > 1000:
            return 6
        elif self.no_change_counter > 600:
            return 4
        elif self.no_change_counter > 400:
            return 2
        else:
            return 1