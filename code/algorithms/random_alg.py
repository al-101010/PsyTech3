import random

from .algorithm import Algorithm


class Random(Algorithm):
    """
    A class to represent a random algorithm.
    """

    def __init__(self, empty_schedule) -> None:
        super().__init__(empty_schedule)
        self.schedule_courses(self.schedule.archive)
        self.schedule_students()

    def pick_random_roomslot(self, archive : list) -> tuple:
        """Pick random roomslot from archive"""
        return random.choice(archive)  
    
    def remove_roomslot(self, archive : list, roomslot : tuple) -> None:
        """Remove roomslot from archive"""
        archive.remove(roomslot)

    def schedule_activity(self, activity, roomslot : tuple, archive : list) -> None:
        """
        Schedule given activity on a roomslot from archive.
        """
        # schedule the activity, and remove roomslot from archive
        activity.schedule(roomslot[0], roomslot[1], roomslot[2])
        self.remove_roomslot(archive, roomslot)

    def schedule_courses(self, archive : list) -> None:
        """
        Schedule all activities on a random roomslot that is available.
        """
        # shuffle activities list
        random.shuffle(self.schedule.activities)

        # loop over all activities and pick a roomslot to schedule it
        for activity in self.schedule.activities:  
           roomslot = self.pick_random_roomslot(archive)
           self.schedule_activity(activity, roomslot, archive)

    def get_random_tutorial(self, activities : list):
        """
        Pick a random tutorial/practical group that is not at full
        capacity from list of activities.
        """
        activity = random.choice(activities)

        # pick a new random group while current group is at full capacity
        while len(activity.students) == activity.capacity:
            activity = random.choice(activities)
        
        return activity
    
    def schedule_student_activity(self, activity, student) -> None:
        """
        Add student to list of students in activity instance, and add
        activity to list of activities in student instance.
        """
        student.activities.add(activity)
        activity.students.add(student)

    def schedule_student_activities(self, activity_type : str, activities : list, student) -> None:       
        """
        Schedule students to relevant activities.
        Picks a random tutorial/practical group in case of tutorial/practical.
        Schedules students to all lectures in case of lecture.
        """    
        # pick a group if activity is not lecture
        if activity_type != 'h':
            activity = self.get_random_tutorial(activities)
            self.schedule_student_activity(activity, student)

        # schedule student to all lectures
        else:
            for activity in activities:
                self.schedule_student_activity(activity, student)
    
    def schedule_students(self) -> None:
        """
        Schedule all students in random activities for the courses they follow.
        """
        # shuffle list of students
        random.shuffle(self.schedule.students)

        # loop over all students and their courses
        for student in self.schedule.students:
            for course in student.courses:

                # schedule students to relevant activities of course
                for activity_type, activities in course.activities.items():
                    self.schedule_student_activities(activity_type, activities, student)
            
        # update the students' personal schedule attribute
        self.update_student_schedules()

class FittedStart(Random):
    """
    A class to represent a fitted start algorithm which avoids starting with room overcapicity
    """
    def schedule_courses(self, archive):
        """
        Schedule all activities on a roomslot that is available and is just
        big enough so there is no overcapacity.
        """
        # sort activities on their capacity limit
        activities = sorted(self.schedule.activities, key=lambda activity: activity.capacity, reverse=True)

        # loop over all activities
        for activity in activities: 

            # initiate space left in room counter
            lowest_space_left = float('inf')
            
            # loop over all available roomslots
            for roomslot in archive:
               
               # calculate the space left if the activity would be scheduled in this room
               space_left = roomslot[0].capacity - activity.capacity

               # keep track of best fitting room
               if space_left > 0 and space_left < lowest_space_left:
                   lowest_space_left = space_left
                   best_roomslot = roomslot
            
            # schedule activity in the best fitting room
            self.schedule_activity(activity, best_roomslot, archive)


