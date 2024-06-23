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

    def pick_activity(self, activities):
        N = math.ceil(len(activities) / 2)
        top_activities = self.get_activities_with_most_maluspoints(activities, N)
        return super().pick_activity(top_activities)

    def pick_student(self, students):
        N = math.ceil(len(students) / 2)
        top_students = self.get_students_with_most_maluspoints(students, N)
        return super().pick_student(top_students)
    
    def pick_students_to_switch(self, students, N):
        return self.get_students_with_most_maluspoints(students, N)
    
    def switch_activities(self):
        """
        Switches the activities from two randomly chosen roomslots. Activity may
        also be None.
        """
        # store room, day, and time of roomslots
        roomslot1, roomslot2 = self.pick_roomslots_to_switch()
        room_1, day_1, time_1 = roomslot1

        # save activities in roomslots
        activity_1 = room_1.schedule[day_1][time_1]
        activity_2, activity_2_type, course_2 = self.pick_activity(self.schedule.activities)

        room_2, day_2, time_2 = (activity_2.room, activity_2.day, activity_2.time)


        # if activity is Activity instance, schedule instance
        if activity_1:
            activity_1.schedule(room_2, day_2, time_2)
        if activity_2:
            activity_2.schedule(room_1, day_1, time_1)
        
        # switch the activities to the other roomslot in room instance
        room_1.schedule[day_1][time_1] = activity_2
        room_2.schedule[day_2][time_2] = activity_1

        self.update_student_schedules()
        
        # update the archive if an activity is switched to an empty spot 
        self.update_archive(activity_1, roomslot1, roomslot2)
        self.update_archive(activity_2, roomslot2, roomslot1)
    
    def mutate_schedule(self, number_of_mutations: int = 1):
        for i in range(number_of_mutations):            
            if self.no_change_counter > 500 and self.schedule.archive:
                mutation = random.choices([self.switch_student_from_activities, self.switch_activities, self.split_activity], weights=(.2, .2, .6))[0]
            elif self.iteration < 1000:
                mutation = random.choices([self.switch_student_from_activities, self.switch_activities], weights=(.2, .8))[0]
            else:
                mutation = random.choices([self.switch_student_from_activities, self.switch_activities], weights=(.8, .2))[0]
            
            mutation()