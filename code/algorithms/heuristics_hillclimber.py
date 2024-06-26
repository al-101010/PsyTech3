import random
import math

from code.classes.schedule import Schedule

from .hillclimber import Hillclimber

class HeuristicsHillclimber(Hillclimber):
    """
    A class representing heuristic hillclimbers.
    """
    def __init__(self, empty_schedule: Schedule, early_stopping: bool = False):
        super().__init__(empty_schedule, early_stopping)

    def get_objects_with_most_maluspoints(self, objects : list, top_n : int=20) -> list:
        """
        Returns a list of the top N objects with most maluspoints.
        """
        return sorted(objects, key=lambda object: object.maluspoints, reverse=True)[:top_n]

    
class ProblematicActivityClimber(HeuristicsHillclimber):
    """
    A class representing the problematic activity heuristic, which selects random activities from those with the most maluspoints whenever
    we need to pick activities for a mutation.
    """
    def __init__(self, empty_schedule: Schedule, early_stopping: bool = False):
        super().__init__(empty_schedule, early_stopping)

    def pick_activity(self, activities : list):
        """
        Returns a random activity from the top 1/3 activities with most maluspoints.
        """
        # set N as 1/3 of the total activities list
        N = math.ceil(len(activities) / 3)

        top_activities = self.get_objects_with_most_maluspoints(activities, N)

        return super().pick_activity(top_activities)
    
class ProblematicStudentsClimber(HeuristicsHillclimber):
    """
    A class representing the problematic students heuristic, which selects random students from those with the most maluspoints whenever
    we need to pick students for a mutation.
    """
    def __init__(self, empty_schedule: Schedule, early_stopping: bool = False):
        super().__init__(empty_schedule, early_stopping)

    def pick_student(self, students : list):
        """
        Returns a random student from the top 1/3 students with most maluspoints.
        """
        # set N as 1/3 of the total students list
        N = math.ceil(len(students) / 3)

        top_students = self.get_objects_with_most_maluspoints(students, N)

        return super().pick_student(top_students)
    
    def pick_students_to_switch(self, students : list, N : int):
        """
        Return N students with most maluspoints
        """
        return self.get_objects_with_most_maluspoints(students, N)
    
class MutationProbabilityClimber(HeuristicsHillclimber):
    """
    A class representing the mutation probability heuristic for which the probability of certain mutations being made shifts/changes
    as the algorithm progresses and (potentially) stagnates.
    """
    def __init__(self, empty_schedule: Schedule, early_stopping: bool = False):
        super().__init__(empty_schedule, early_stopping)
    
    def mutate_schedule(self, number_of_mutations : int = 1):
        """
        Mutate the schedule for a specified number of times, varying the
        mutation probability depending on the iteration and no_change_counter.
        """

        # loop for the number of mutations
        for i in range(number_of_mutations):     

            # only try adding activities if algorithm is stuck and roomslots are available      
            if self.no_change_counter > 500 and self.schedule.archive:
                mutation = random.choices([self.switch_student_from_activities, self.switch_activities, self.add_activity_to_course], weights=(.2, .2, .6))[0]
            
            # try switching activities more in early iterations and students in later iterations
            elif self.iteration < 1000:
                mutation = random.choices([self.switch_student_from_activities, self.switch_activities], weights=(.2, .8))[0]
            else:
                mutation = random.choices([self.switch_student_from_activities, self.switch_activities], weights=(.8, .2))[0]
            
            mutation()

class IncreasingMutationsClimber(HeuristicsHillclimber):
    """
    A class representing the increasing mutations heuristic for which the number of mutations made to the schedule increases 
    as the algorithm progresses.
    """
    def __init__(self, empty_schedule: Schedule, early_stopping: bool = False):
        super().__init__(empty_schedule, early_stopping)
        
    def pick_number_mutations(self):
        """
        Returns the number of mutations to be done.
        """

        # try more mutations as the algorithm is stuck longer
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