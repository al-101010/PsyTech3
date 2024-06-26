class Activity:
    """
    A class to represent an activity.

    . . .

    Attributes
    ----------
    name: str
        name of the activity (activity type and number)
    capacity: int
        how many students fit/are allowed in this activity
    course: Course
        what course (object) this activity is a part of
    students: set[Student]
        a set of all students signed up for this activity
    maluspoints: int
        score representitive of the number of student double bookings this activity is involved with
    """
    
    def __init__(self, name : str, capacity : int, course) -> None:
        self.name = name
        self.capacity = capacity
        self.course = course
        self.students = set()
        self.maluspoints = 0


    def __repr__(self) -> str:
        return f'{self.name} from {self.course}'


    def schedule(self, room, day, time) -> None:
        """
        Schedule this activity on the given day and time to given room.
        """
        self.room = room
        self.day = day
        self.time = time

        room.schedule[day][time] = self 

    def reset_maluspoints(self) -> None:
        """
        Resets this activity's maluspoints to 0.
        """
        self.maluspoints = 0

    def is_full(self) -> bool:
        """
        Returns true if activity is at full capacity.
        """
        return len(self.students) >= self.capacity
    
    def is_tutorial_practical(self) -> bool:
        """
        Returns true if actvity is a tutorial or practical.
        """
        return 'w' in self.name or 'p' in self.name
    
    def get_roomslot(self) -> None:
        """
        Returns the roomslot this activity is scheduled in.
        """
        return self.room, self.day, self.time
        