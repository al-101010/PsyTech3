import random
import math
import matplotlib.pyplot as plt

from .hillclimber import Hillclimber
from ..classes.schedule import Schedule

class TargetedHillclimber(Hillclimber):
    def get_activities_with_most_maluspoints(self, top_n: int=20) -> list:
        return sorted(self.schedule.activities, key=lambda activity: activity.maluspoints, reverse=True)[:top_n]
    
    def get_students_with_most_maluspoints(self, top_n: int=20) -> list:
        return sorted(self.schedule.students, key=lambda student: student.maluspoints, reverse=True)[:top_n]

    def pick_roomslots_to_switch(self):
        """
        Returns two random roomslots.
        """
        # pick roomslots to switch activities from
        random_roomslot1 = random.choice(self.schedule.roomslots)
        random_roomslot2 = random.choice(self.schedule.roomslots)

        return random_roomslot1, random_roomslot2
    
    def get_random_activity(self):
        """
        Returns the course, activity type, and activity instance of a 
        randomly chosen tutorial or practical that has at least one
        other activity of that same type.
        """
         # pick a random course
        random_course = random.choice(self.schedule.courses)
        
        # make sure the course has tutorials or practicals
        while not ('w' or 'p') in random_course.activities:
            random_course = random.choice(self.schedule.courses)

        # choose random activity type
        random_activity_type = random.choice(list(random_course.activities))

        # make sure activity type has more than 1 activities and is not a lecture
        while len(random_course.activities[random_activity_type]) <= 1 or random_activity_type == 'h':
            random_activity_type = random.choice(list(random_course.activities))

        # pick a random tutorial or practical
        random_activity = random.choice(random_course.activities[random_activity_type])

        # make sure activity has students
        while len(random_activity.students) == 0:
            random_activity = random.choice(random_course.activities[random_activity_type])


        return random_course, random_activity_type, random_activity

    def switch_activities(self):
        """
        Switches the activities from two randomly chosen roomslots. Activity may
        also be None.
        """
        # store room, day, and time of roomslots
        random_roomslot1, random_roomslot2 = self.pick_roomslots_to_switch()
        room_1, day_1, time_1 = self.get_roomslot_info(random_roomslot1)
        room_2, day_2, time_2 = self.get_roomslot_info(random_roomslot2)

        # save activities in roomslots
        activity_1 = room_1.schedule[day_1][time_1]
        activity_2 = room_2.schedule[day_2][time_2]

        # if activity is Activity instance, schedule instance
        if activity_1:
            activity_1.schedule(room_2, day_2, time_2)
        if activity_2:
            activity_2.schedule(room_1, day_1, time_1)
        
        # switch the activities to the other roomslot in room instance
        room_1.schedule[day_1][time_1] = activity_2
        room_2.schedule[day_2][time_2] = activity_1

        self.update_student_schedules()
        
        """ Still in progress. """
        # self.update_archive(activity_1, activity_2, room_1, day_1, time_1, room_2, day_2, time_2)
    
        
    def switch_student_from_activities(self):
        """
        Switches a random student from one of their current activities to 
        another activity of the same type in the same course. 
        """
        ##TODO: I still need to implement switching two students if an activity is full

        random_course, random_activity_type, random_activity = self.get_random_activity()

        # pick a random students from the tutorial/practical
        random_student = random.choice(sorted(random_activity.students, key=lambda student: student.maluspoints, reverse=True)[:10])

        # pick another random activity to switch student to
        switch_activity = random.choice(random_course.activities[random_activity_type])

        # pick new activity if new activity is same as random activity
        while switch_activity == random_activity:
            switch_activity = random.choice(random_course.activities[random_activity_type])

        # move the student to the new activity if activity is not full
        if not len(switch_activity.students) == switch_activity.capacity:
            self.move_student(random_student, random_activity, switch_activity)

        # if the other tutorial is full pick another or switch students?
