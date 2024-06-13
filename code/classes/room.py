
class Room:

    def __init__(self, room_number : str, capacity : str) -> None:
        self.room_number = room_number
        self.capacity = capacity

        self.empty_schedule()


    def __repr__(self) -> str:
        return self.room_number


    def empty_schedule(self, days : list[str] = ['ma', 'di', 'wo', 'do', 'vr'], timeslots : list[str] = ['9', '11', '13', '15']):
        """
        Create an empty schedule for this room, all timeslots are labeled 'free'.
        """

        # give evening slot to biggest room
        # TO DO: is dit hardcoden?
        if self.room_number == 'C0.110':
            timeslots.append('17')
        else:
            timeslots = ['9', '11', '13', '15']

        self.timeslots = timeslots
        self.days = days

        self.schedule = {}

        # loop over each day and create a key
        for day in days:
            self.schedule[day] = {}

            # loop over each time slot and label it 'free'
            for timeslot in timeslots:
                self.schedule[day][timeslot] = []
