class Activity:

    def __init__(self, name : str, capacity : str, course) -> None:
        self.name = name
        self.capacity = capacity
        self.course = course
        self.scheduled = False


    def __repr__(self) -> str:
        return f'{self.name} from {self.course}'


    def schedule(self, room, day, time):
        """
        Schedule this activity on the given day and time to given room.
        """
        self.room = room
        self.day = day
        self.time = time
        self.scheduled = True