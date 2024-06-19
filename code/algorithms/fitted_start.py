import random
import copy

from .algorithm import Algorithm
from .random_alg import Random

class FittedStart(Random):

    def schedule_courses(self, archive):
        """
        Schedule all activities on a random roomslot that is available.
        """
        activities = sorted(self.schedule.activities, key=lambda activity: activity.capacity, reverse=True)


        # loop over all activities
        for activity in activities:  
            lowest_space_left = float('inf')
            for roomslot in archive:
               space_left = roomslot[0].capacity - activity.capacity
               if space_left > 0 and space_left < lowest_space_left:
                   lowest_space_left = space_left
                   best_roomslot = roomslot
            self.schedule_activity(activity, best_roomslot, archive)

    # def schedule_student_activities(self, activity_type, activities, student):       
    #     """
    #     Schedule students to relevant activities.
    #     Picks a random tutorial/practical group in case of tutorial/practical.
    #     Schedules students to all lectures in case of lecture.
    #     """    
    #     if activity_type != 'h':
    #         for activity in activities:
    #             if not (student.schedule[activity.day][activity.time] and not (len(activity.students) >= activity.capacity)):
    #                 self.schedule_student_activity(activity, student)
    #                 student.update_schedule()
    #                 break
    #         activity = self.get_random_tutorial(activities)
    #         self.schedule_student_activity(activity, student) 
    #     else:
    #         # schedule student to all lectures
    #         for activity in activities:
    #             self.schedule_student_activity(activity, student)
        
    #     student.update_schedule()