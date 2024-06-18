import random
import copy

from .algorithm import Algorithm

##TODO: remove random seed comments

class Random(Algorithm):
    random.seed(1)

    def __init__(self, empty_schedule) -> None:
        super().__init__(empty_schedule)
        self.schedule_courses(self.archive)
        self.schedule_students()

    def pick_random_roomslot(self, archive):
        """Pick random roomslot from archive"""
        random.seed(1)
        return random.choice(archive)  
    
    def remove_roomslot(self, archive, roomslot):
        """Remove roomslot from archive"""
        archive.remove(roomslot)

    def schedule_activity(self, activity, roomslot, archive):
        """
        Schedule given activity on a roomslot from archive.
        """
        # schedule the activity, and remove roomslot from archive
        activity.schedule(roomslot[0], roomslot[1], roomslot[2])
        self.remove_roomslot(archive, roomslot)

    def schedule_courses(self, archive):
        """
        Schedule all activities on a random roomslot that is available.
        """
        random.seed(1)
        random.shuffle(self.schedule.activities)

        # loop over all activities
        for activity in self.schedule.activities:  
           roomslot = self.pick_random_roomslot(archive)
           self.schedule_activity(activity, roomslot, archive)

    def get_random_tutorial(self, activities):
        """
        Pick a random tutorial/practical group that is not at full
        capacity from list of activities.
        """
        random.seed(1)
        activity = random.choice(activities)

        # pick a new random group while current group is at full capacity
        while len(activity.students) == activity.capacity:
            activity = random.choice(activities)
        
        return activity
    
    def schedule_student_activity(self, activity, student):
        """
        Add student to list of students in activity instance, and add
        activity to list of activities in student instance.
        """
        student.activities.add(activity)
        activity.students.add(student)

    def schedule_student_activities(self, activity_type, activities, student):       
        """
        Schedule students to relevant activities.
        Picks a random tutorial/practical group in case of tutorial/practical.
        Schedules students to all lectures in case of lecture.
        """    
        if activity_type != 'h':
            activity = self.get_random_tutorial(activities)
            self.schedule_student_activity(activity, student)
        else:
            # schedule student to all lectures
            for activity in activities:
                self.schedule_student_activity(activity, student)
    
    def schedule_students(self):
        """
        Schedule all students in random activities for the courses they follow.
        """
        random.seed(1)
        random.shuffle(self.schedule.students)

        # loop over all students and their courses
        for student in self.schedule.students:
            for course in student.courses:
                for activity_type, activities in course.activities.items():
                    self.schedule_student_activities(activity_type, activities, student)
            
        # update the students' personal schedule attribute
        self.update_student_schedules()



