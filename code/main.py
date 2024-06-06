import sequential as seq
import classes as cl
import pandas as pd

def get_output(students : list[cl.Student]):
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

        schedule.to_csv('../data/test_output.csv', index=False)

        return schedule


if __name__ == "__main__":
    # represent empty schedule from data
    test_schedule = cl.Schedule('../data/studenten_en_vakken.csv', '../data/vakken.csv', '../data/zalen.csv')

    # create schedule using sequential algorithm
    sequential_schedule = seq.Sequential(test_schedule)
    sequential_schedule.schedule_courses()
    sequential_schedule.schedule_students()
    print(get_output(test_schedule.students))