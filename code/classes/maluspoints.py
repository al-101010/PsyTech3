
class Maluspoints:
    def __init__(self, students: list):
        self.total_maluspoints = 0

        # for now only calculated from empty slots
        self.students_maluspoints(students)
        self.evening_room_maluspoints()

    def students_maluspoints(self, students: list):
        """
        Takes in a list of scheduled students and calculates the total amount
        of maluspoints. Add double bookings!
        """

        # loop over each student
        for student in students:
            # add their maluspoints to the total
            self.total_maluspoints += student.maluspoints

        return self.total_maluspoints

    def evening_room_maluspoints(self):
        """
        Calculates maluspoints for usage of evening slot. Finalize.
        """
        pass