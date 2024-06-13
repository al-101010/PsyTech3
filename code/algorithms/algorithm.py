import random

class Algorithm:

    def __init__(self, schedule):
        self.final_schedule = schedule
        self.final_maluspoints = schedule.total_maluspoints

    def update_student_schedules(self):
        for student in self.schedule.students:
            student.personal_schedule()

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

    def mutate_schedule(self):
        """
        Mutate current schedule/timetable with a random action
        INCOMPLETE -> need to add more ways to alter the schedule
        = Useful when we have multiple ways of altering the schedule (as we don't want to make every
        single alteration at ones)
        """

        chance = random.random()

        if chance < 1:
            self.switch_activities()
        # elif 0.5 <= chance < 0.8:
        #     move student to other practical
        #     or redistribute all students

    def run(self):
        raise NotImplementedError