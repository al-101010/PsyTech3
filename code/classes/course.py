import math
from .activity import Activity
from .student import Student

class Course:

    def __init__(self, name : str, students : list[Student], activity_amounts : dict) -> None:
        self.name = name
        self.students = students
        self.activity_amounts = activity_amounts
        self.activities = {}

        self.add_activities(activity_amounts)


    def __repr__(self) -> str:
        return self.name


    def add_activities(self, activity_amounts : dict[str : int]):
        """
        Add all course activities to a dictionary. Accepts a dictionary
        with activities ('h', 'w', 'p') as keys and an amount as value.
        """
        # loop over all activity types to be created
        for activity_type, (amount, capacity) in activity_amounts.items():
            # do not add activities with 0 amount
            if amount == 0:
                continue

            # lectures do not have a capacity so next line not needed
            if not 'h' in activity_type:

                # calculate how many activities of this type are needed by capacity
                amount = math.ceil(len(self.students) / capacity)

            # loop over number of activities of this type
            for i in range(1, amount + 1):
                name = f'{activity_type}{i}'

                # create dictionary key for this activity type and append activity instance to list
                if activity_type in self.activities:
                    self.activities[activity_type].append(Activity(name, capacity, self))
                else:
                    self.activities[activity_type] = [(Activity(name, capacity, self))]
