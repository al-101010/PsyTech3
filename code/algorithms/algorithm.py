import random

class Algorithm:

    def __init__(self, schedule):
        self.final_schedule = schedule
        self.final_maluspoints = schedule.total_maluspoints

    def switch_activities(self):
        """
        Switches the activities from two randomly chosen roomslots. Activity may
        also be 'Free'.
        """
        # pick roomslots to switch activities from
        random_roomslot1 = random.choice(self.schedule.roomslots)
        random_roomslot2 = random.choice(self.schedule.roomslots)

        # save activities as variables
        activity_1 = random_roomslot1[0].schedule[random_roomslot1[1]][random_roomslot1[2]]
        activity_2 = random_roomslot2[0].schedule[random_roomslot2[1]][random_roomslot2[2]]

        # switch the activities to the other roomslot
        random_roomslot1[0].schedule[random_roomslot1[1]][random_roomslot1[2]] = activity_2
        random_roomslot2[0].schedule[random_roomslot2[1]][random_roomslot2[2]] = activity_1