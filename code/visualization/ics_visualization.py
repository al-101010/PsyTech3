import pandas as pd

def get_start_end_time(timeslot : int) -> tuple[int, int]:
    """
    Returns the start and end time of given timeslot
    """
    # add a 0 if timeslot has only one number
    if len(str(timeslot)) == 1:
        start_time = '0' + str(timeslot)
    else: 
        start_time = timeslot

    # timeslot is always two hours
    end_time = timeslot + 2

    return start_time, end_time

def write_course_schedules(data_file : str='../../results/hillclimber/tested_hillclimber_output_500K.csv'):
    """
    Write ICS file for each course in the given data file, each activity gets it's
    own event. The files are written to the course_schedules folder.
    """
    # create dataframe and group by course activities
    df = pd.read_csv(data_file)
    group_courses = df.groupby(['Vak', 'Activiteit'])

    # get day, time, room and students of each activity
    unique_values = group_courses.agg({
    'Tijdslot': lambda x: x.unique().tolist(),
    'Zaal': lambda x: x.unique().tolist(),
    'Dag': lambda x: x.unique().tolist(),
    'Student': lambda x: x.unique().tolist()
    }).reset_index()

    # map each day to a date (chose a week in june for this)
    day_to_date = {'ma' : 24, 'di' : 25, 'wo' : 26, 'do' : 27, 'vr' : 28}

    # loop over each course and create ICS file 
    for course in pd.unique(df['Vak']):
        with open(f"course_schedules/{course}.ics", 'w') as f:
            f.write("BEGIN:VCALENDAR\nVERSION:2.0\n")

            # add each activity of this course as an event in ICS file
            for index, row in unique_values.iterrows():
                if course == row['Vak']:
                    start_time, end_time = get_start_end_time(row['Tijdslot'][0])
                    
                    # add activity information to file
                    f.write(f"BEGIN:VEVENT\n")
                    f.write(f"SUMMARY:{row['Activiteit']} - {row['Vak']}\n")
                    f.write(f"DTSTART;TZID=Europe/Brussels:202406{day_to_date[row['Dag'][0]]}T{start_time}0000\n")
                    f.write(f"DTEND;TZID=Europe/Brussels:202406{day_to_date[row['Dag'][0]]}T{end_time}0000\n")
                    f.write(f"LOCATION:{row['Zaal'][0]}\n")
                    f.write(f"DESCRIPTION:{', '.join(row['Student'])}\n")
                    f.write(f"END:VEVENT\n")
            
            f.write('END:VCALENDAR')
            f.close()

if __name__ == "__main__":
    write_course_schedules()


