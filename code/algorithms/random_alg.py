import random

class Random:

    def __init__(self, schedule) -> None:
        self.schedule = schedule
        self.schedule_courses()
        self.schedule_students()

    def schedule_courses(self):
        archive = []

        #TO DO: add set of all combinations
        for room in self.schedule.rooms:
            for day in room.days:
                for time in room.timeslots:
                    archive.append((room, day, time))

        for activity in self.schedule.activities:  
            room_slot = random.choice(archive)  
            room = room_slot[0]
            day = room_slot[1]
            time = room_slot[2]

            activity.schedule(room, day, time)
            archive.remove(room_slot)

    def schedule_students(self):
        for student in self.schedule.students:
            for course in student.courses:
                for activity_type, activities in course.activities.items():
                    if activity_type != 'h':
                        activity = random.choice(activities)

                        while len(activity.students) == activity.capacity:
                            activity = random.choice(activities)

                        student.activities.add(activity)
                        activity.students.add(student)
                    else:
                        for activity in activities:
                            student.activities.add(activity)
                            activity.students.add(student)
            
            student.personal_schedule()

            # calculate malus_points
            student.get_malus_points(student.schedule)
