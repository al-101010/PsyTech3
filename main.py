from code.algorithms.sequential import Sequential # Ignore : True
from code.algorithms.random_alg import Random
from code.classes.schedule import Schedule
from code.classes.maluspoints import Maluspoints
import pandas as pd

def get_output(students : list, output : str):
        """
        Print output schedule as data frame and convert to csv.
        """
        rows = []

        # loop over all activities of each student and append relevant info
        for student in students:
            for activity in student.activities:
                rows.append([student.name, activity.course, activity.name, activity.room.room_number, activity.day, activity.time])

        # create dataframe of schedule
        schedule = pd.DataFrame(rows, columns=['Student', 'Vak', 'Activiteit', 'Zaal', 'Dag', 'Tijdslot'])

        schedule.to_csv(output, index=False)

        return schedule


if __name__ == "__main__":
    # represent empty schedule from data
    test_schedule = Schedule('data/studenten_en_vakken.csv', 'data/vakken.csv', 'data/zalen.csv')

    # create schedule using sequential algorithm
    sequential_schedule = Sequential(test_schedule)
    sequential_schedule.schedule_courses()
    sequential_schedule.schedule_students()

    # create schedule using random algorithm
    random_schedule = Random(test_schedule)

    # calculate malus points
    maluspoints = Maluspoints(sequential_schedule.schedule.students)
    print(f"This schedule resulted in {maluspoints.total_maluspoints} maluspoints from empty time slots.")

    # print(get_output(test_schedule.students, 'data/test_output.csv'))

    print(get_output(test_schedule.students, 'data/random_output.csv'))
