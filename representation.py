class Student:
    
    def __init__(self, name : str, number : str, subject_names = set[str]) -> None:
        self.name = name
        self.student_number = number
        self.subject_names = subject_names
        self.subjects = set()

    def add_subjects(self, all_subjects : set):
        """
        Add a student's subjects to the set of subjects as a Subject class.
        Also removes NA values.
        """
        for subject in all_subjects:
            if subject.name in self.subject_names:
                self.subjects.add(subject)


class Subject:
    
    def __init__(self, name : str, students : list[Student]) -> None:
        self.name = name

    def add_activities(self):
        pass

class Activity:
    def __init__(self, name : str, max_students : str) -> None:
        pass

class Room:

    def __init__(self, room_number : str, capacity : str) -> None:
        self.room_number = room_number
        self.capacity = capacity




        
class Day:
    pass