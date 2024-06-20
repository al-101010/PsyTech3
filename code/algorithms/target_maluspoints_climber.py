import random
import math
import matplotlib.pyplot as plt

from .hillclimber import Hillclimber
from ..classes.schedule import Schedule

class TargetMaluspointsClimber(Hillclimber):
    def get_activities_with_most_maluspoints(self, activities, top_n: int=20) -> list:
        return sorted(activities, key=lambda activity: activity.maluspoints, reverse=True)[:top_n]
    
    def get_activities_with_least_maluspoints(self, activities, top_n: int=20):
        return sorted(activities, key=lambda activity: activity.maluspoints, reverse=False)[:top_n]
         
    def get_students_with_most_maluspoints(self, students, top_n: int=20) -> list:
        return sorted(students, key=lambda student: student.maluspoints, reverse=True)[:top_n]
    
    def get_activity(self, student):
            """
            Returns the course, activity type, and activity instance of a 
            chosen tutorial or practical that has at least one
            other activity of that same type.
            """
            # pick a random tutorial or practical
            activity = random.choice(list(student.activities))
            course = activity.course
            activity_type = activity.name[0]

            # make sure activity has students and multiple activities
            while len(course.activities[activity_type]) < 2:
                activity = random.choice(list(student.activities))
                course = activity.course
                activity_type = activity.name[0]

            return course, activity_type, activity

    def get_student(self):
         return random.choice(self.get_students_with_most_maluspoints(self.schedule.students))

    def switch_student_from_activities(self):
            """
            Switches a random student from one of their current activities to 
            another activity of the same type in the same course. 
            """

            # pick a random students from the tutorial/practical
            student = self.get_student()
            course, activity_type, activity = self.get_activity(student)

            # pick another random activity to switch student to
            switch_activity = random.choice(course.activities[activity_type])

            # pick new activity if new activity is same as random activity
            while switch_activity == activity:
                switch_activity = random.choice(course.activities[activity_type])

            # move another student to this activity if new activity is full
            if len(switch_activity.students) == switch_activity.capacity:
                switch_student = random.choice(list(switch_activity.students))
                self.move_student(switch_student, switch_activity, activity)
            
            # move this student to other activity
            self.move_student(student, activity, switch_activity)

    # def switch_activities(self):
    #     """
    #     Switches the activities from two randomly chosen roomslots. Activity may
    #     also be None.
    #     """
    #     # save activities in roomslots
    #     activity_1 = random.choice(self.get_activities_with_most_maluspoints(self.schedule.activities))
    #     activity_2 = random.choice(self.get_activities_with_least_maluspoints(self.schedule.activities))

    #     while activity_1 == activity_2:
    #         activity_1 = random.choice(self.get_activities_with_most_maluspoints(self.schedule.activities))
    #         activity_2 = random.choice(self.get_activities_with_least_maluspoints(self.schedule.activities))

    #     room_1, day_1, time_1 = activity_1.room, activity_1.day, activity_1.time
    #     room_2, day_2, time_2 = activity_2.room, activity_2.day, activity_2.time

    #     # if activity is Activity instance, schedule instance
    #     if activity_1:
    #         activity_1.schedule(room_2, day_2, time_2)
    #     if activity_2:
    #         activity_2.schedule(room_1, day_1, time_1)

    #     # switch the activities to the other roomslot in room instance
    #     room_1.schedule[day_1][time_1] = activity_2
    #     room_2.schedule[day_2][time_2] = activity_1

    #     self.update_student_schedules()