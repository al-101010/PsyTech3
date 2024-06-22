class Activity:

    def __init__(self, name : str, capacity : str, course) -> None:
        self.name = name
        self.capacity = capacity
        self.course = course
        self.students = set()
        self.maluspoints = 0


    def __repr__(self) -> str:
        return f'{self.name} from {self.course}'


    def schedule(self, room, day, time):
        """
        Schedule this activity on the given day and time to given room.
        """
        self.room = room
        self.day = day
        self.time = time

        room.schedule[day][time] = self 

    def reset_maluspoints(self):
        self.maluspoints = 0

    def is_full(self):
        return len(self.students) >= self.capacity
    
    def is_tutorial_practical(self):
        return 'w' in self.name or 'p' in self.name
    
    def get_roomslot(self):
        return self.room, self.day, self.time
        