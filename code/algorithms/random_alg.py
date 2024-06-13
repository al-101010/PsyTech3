import random
import copy

class Random:
    # random.seed(1)

    def __init__(self, schedule) -> None:
        self.schedule = copy.deepcopy(schedule)
        self.schedule_courses()
        self.schedule_students()

    def get_room_slots(self):
        """Create archive of all possible roomslots"""
        # empty list for archive of all room-slots
        archive = []

        # add all room-slots to archive
        for room in self.schedule.rooms:
            for day in room.days:
                for time in room.timeslots:
                    archive.append((room, day, time))

        return archive

    def pick_random_room_slot(self, archive):
        """Pick random roomslot from archive"""
        # random.seed(1)

        return random.choice(archive)  

    
    def remove_room_slot(self, archive, room_slot):
        """Remove roomslot from archive"""
        archive.remove(room_slot)

    def schedule_courses(self):
        """
        Schedule all activities on random days, timeslots and rooms.
        """
        # random.seed(1)
        archive = copy.copy(self.schedule.roomslots)

        random.shuffle(self.schedule.activities)

        # loop over all activities
        for activity in self.schedule.activities:  
            room_slot = self.pick_random_room_slot(archive)
            activity.schedule(room_slot[0], room_slot[1], room_slot[2])

            self.remove_room_slot(archive, room_slot)

    def get_random_tutorial(self, activities):
        # random.seed(1)

        # if activity is not a lecture, pick a random group
        activity = random.choice(activities)

        # pick a new random group while current group is at full capacity
        while len(activity.students) == activity.capacity:
            activity = random.choice(activities)
        
        return activity
    
    def schedule_student_activity(self, activity, student):
        student.activities.add(activity)
        activity.students.add(student)

    def schedule_student_activities(self, activity_type, activities, student):           
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
        # random.seed(1)

        random.shuffle(self.schedule.students)
        # loop over all students and their courses
        for student in self.schedule.students:
            for course in student.courses:
                for activity_type, activities in course.activities.items():
                    self.schedule_student_activities(activity_type, activities, student)
            
            # update the student's personal schedule attribute
            student.personal_schedule()



