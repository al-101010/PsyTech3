import random

class Random:

    def __init__(self, schedule) -> None:
        self.schedule = schedule
        self.schedule_courses()
        self.schedule_students

    def schedule_courses(self):
        
        for course in self.schedule.courses:
            for activities in course.activities.values():
                for activity_instance in activities:
                    room = random.choice(self.schedule.rooms)
                    day = random.choice(['Ma', 'Di', 'Wo', 'Do', 'Vr'])
                    time = random.choice(['9', '11', '13', '15'])

                    activity_instance.schedule(room, day, time)

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
            student.get_malus_points(student.schedule)
