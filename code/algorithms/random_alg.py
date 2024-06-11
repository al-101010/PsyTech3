import random

class Random:

    def __init__(self, schedule) -> None:
        self.schedule = schedule
        self.schedule_courses()
        self.schedule_students()

    def schedule_courses(self):
        """
        Schedule all activities on random days, timeslots and rooms.
        """
        # empty list for archive of all room-slots
        archive = []

        # add all room-slots to archive
        for room in self.schedule.rooms:
            for day in room.days:
                for time in room.timeslots:
                    archive.append((room, day, time))

        # loop over all activities
        for activity in self.schedule.activities:  

            # pick random room-slot to schedule this activity
            room_slot = random.choice(archive)  
            room = room_slot[0]
            day = room_slot[1]
            time = room_slot[2]
            activity.schedule(room, day, time)

            # remove room-slot from archive
            archive.remove(room_slot)

    def schedule_students(self):
        """
        Schedule all students in random activities for the courses they follow.
        """
        # loop over all students and their courses
        for student in self.schedule.students:
            for course in student.courses:
                for activity_type, activities in course.activities.items():

                    # if activity is not a lecture, pick a random group
                    if activity_type != 'h':
                        activity = random.choice(activities)

                        # pick a new random group while current group is at full capacity
                        while len(activity.students) == activity.capacity:
                            activity = random.choice(activities)

                        # add students and activities together
                        student.activities.add(activity)
                        activity.students.add(student)
                    else:
                        # schedule student to all lectures
                        for activity in activities:
                            student.activities.add(activity)
                            activity.students.add(student)
            
            # update the student's personal schedule attribute
            student.personal_schedule()

            # calculate malus_points
            student.get_malus_points(student.schedule)
