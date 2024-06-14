import random
import copy
from ..classes.schedule import Schedule

class Algorithm:

    def __init__(self, schedule : Schedule, early_stopping_limit=1000):
        self.schedule = copy.deepcopy(schedule)
        self.archive = copy.copy(self.schedule.roomslots)
        self.maluspoints = schedule.total_maluspoints
        self.early_stopping_limit = early_stopping_limit
        self.no_improvement_counter = 0

    def update_student_schedules(self):
        """
        Update all stutdents' schedules
        """
        for student in self.schedule.students:
            student.update_schedule()

    def switch_activities(self):
        """
        Switches the activities from two randomly chosen roomslots. Activity may
        also be 'Free'.
        """
        # pick roomslots to switch activities from
        random_roomslot1 = random.choice(self.schedule.roomslots)
        random_roomslot2 = random.choice(self.schedule.roomslots)

        room_1 = random_roomslot1[0]
        day_1 = random_roomslot1[1]
        time_1 = random_roomslot1[2]

        room_2 = random_roomslot2[0]
        day_2 = random_roomslot2[1]
        time_2 = random_roomslot2[2]

        # save activities as variables
        activity_1 = room_1.schedule[day_1][time_1]
        activity_2 = room_2.schedule[day_2][time_2]

        if activity_1:
            activity_1.schedule(room_2, day_2, time_2)

        if activity_2:
            activity_2.schedule(room_1, day_1, time_1)
        
        # switch the activities to the other roomslot
        random_roomslot1[0].schedule[random_roomslot1[1]][random_roomslot1[2]] = activity_2
        random_roomslot2[0].schedule[random_roomslot2[1]][random_roomslot2[2]] = activity_1

        self.update_student_schedules()

    def move_student(self, student, current_activity, switch_activity):
        student.activities.remove(current_activity)
        student.activities.add(switch_activity)
        student.update_schedule()

        current_activity.students.remove(student)
        switch_activity.students.add(student)

    def get_random_activity(self):
         # pick a random course
        random_course = random.choice(self.schedule.courses)
        
        # make sure the course has tutorials or practicals
        while not ('w' or 'p') in random_course.activities:
            random_course = random.choice(self.schedule.courses)

        # choose random activity type
        random_activity_type = random.choice(list(random_course.activities))

        while len(random_course.activities[random_activity_type]) <= 1 or random_activity_type == 'h':
            random_activity_type = random.choice(list(random_course.activities))

        # pick a random tutorial or practical
        random_activity = random.choice(random_course.activities[random_activity_type])

        return random_course, random_activity_type, random_activity


    def switch_student_from_activities(self):
        ##NOTE: I still need to check if this works as intended

        random_course, random_activity_type, random_activity = self.get_random_activity()

        # pick a random students from the tutorial/practical
        random_student = random.choice(list(random_activity.students))

        # pick another random activity to switch student to
        switch_activity = random.choice(random_course.activities[random_activity_type])

        while switch_activity == random_activity:
            switch_activity = random.choice(random_course.activities[random_activity_type])

        # move the student to one of the other tutorials/practicals if activity is not full
        if not len(switch_activity.students) == switch_activity.capacity:
            self.move_student(random_student, random_activity, switch_activity)

        # if the other tutorial is full pick another or switch students?


    def mutate_schedule(self, number_of_mutations : int=1):
        """
        Mutate current schedule/timetable with a random action
        INCOMPLETE -> need to add more ways to alter the schedule
        = Useful when we have multiple ways of altering the schedule (as we don't want to make every
        single alteration at ones)
        """

        for i in range(number_of_mutations):
            mutation = random.choice([self.switch_student_from_activities, self.switch_activities])

            mutation()

        # chance = random.random()

        # if chance < 1:
        #     self.switch_activities()
        # elif 0.5 <= chance < 0.8:
        #     move student to other practical
        #     or redistribute all students

    def run(self):
        raise NotImplementedError