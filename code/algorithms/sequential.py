import random

class Sequential:

    def __init__(self, schedule) -> None:
        self.schedule = schedule
        self.maluspoints = 0

    def schedule_courses(self):
        for course in self.schedule.courses:
            for activities in course.activities.values():
                for activity_instance in activities:
                    for room in self.schedule.rooms:
                        for day, timeslots in room.schedule.items():
                            for timeslot, availability in timeslots.items():
                                while activity_instance.scheduled == False:
                                    if availability == 'Free':
                                        room.schedule[day][timeslot] = 'Occupied'
                                        activity_instance.schedule(room, day, timeslot)
                                    else:
                                        break

        # get maluspoints for using the evening slot
        room_maluspoints = self.schedule.get_room_maluspoints()
        self.maluspoints += room_maluspoints


    def schedule_students(self):

        for student in self.schedule.students:
            for course in student.courses:
                for activity_type, activities in course.activities.items():
                    if activity_type != 'h':
                        activity = random.choice(activities)
                        student.activities.add(activity)
                    else:
                        for activity in activities:
                            student.activities.add(activity)
            student.personal_schedule()

            # calculate malus_points
            student_maluspoints = student.get_malus_points(student.schedule)
            self.maluspoints += student_maluspoints
