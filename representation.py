class Subject:
    
    def __init__(self, name : str) -> None:
        self.name = name

class Room:

    def __init__(self, room_number : str, capacity : str) -> None:
        self.room_number = room_number
        self.capacity = capacity

class Activity:
    pass

class Student:
    
    def __init__(self, name : str, number : str, subject_names = list[str]) -> None:
        self.name = name
        self.student_number = number
        self.subjects = []
        
class Day:
    pass