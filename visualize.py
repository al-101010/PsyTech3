import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tabulate
from tabulate import tabulate as tabulate_data

def print_timetable_for_student(timetable_file, student_name: str) -> None:
    """
    Function that takes a csv file containing all information 
    """
    # initialize variables
    timeslots = [9, 11, 13, 15, 17]
    days = ['ma', 'di', 'wo', 'do', 'vr']

    # load in data
    timetable_df = pd.read_csv(timetable_file)

    # filter for student
    student_df = timetable_df[timetable_df['student'] == student_name]
    student_df['alle_info'] = student_df['vak'] + ' - ' + student_df['activiteit'] + ' - ' + student_df['zaal']

    schedule = pd.pivot_table(student_df, values='alle_info', index='tijdslot', columns='dag', aggfunc=lambda x: '\n'.join(x))
    schedule = schedule.reindex(index=timeslots, columns=days)
    schedule.fillna('', inplace=True)

    tabulated_schedule = tabulate_data(schedule, headers='keys', tablefmt='fancy_grid', showindex='always')
    print(f"Weekrooster voor {student_name}:\n")
    print(tabulated_schedule)

def obtain_course_schedule(timetable_file, course_name):
    """
    Function that takes a csv file containing all scheduling information, as well as a 
    string containing the name of a course, and prints the weekly schedule for said
    course
    """
    timeslots = [9, 11, 13, 15, 17]
    days = ['ma', 'di', 'wo', 'do', 'vr']

    # load in data
    df = pd.read_csv(timetable_file)

    course_df = df.groupby('vak').get_group(course_name)
    course_df['alle_info'] = course_df['activiteit'] + ' - ' + course_df['zaal']

    # TO DO: implement way to avoid duplicates
    course_schedule = pd.pivot_table(course_df, values='alle_info', index='tijdslot', columns='dag', aggfunc=lambda x: '\n'.join(x))
    course_schedule = course_schedule.reindex(index=timeslots, columns=days)
    course_schedule.fillna('', inplace=True)

    table = tabulate_data(course_schedule, headers='keys', tablefmt='fancy_grid', showindex='always')

    print(f"Weekrooster voor {course_name} \n")
    print(table)


print_timetable_for_student('test.csv', 'Marleen')
obtain_course_schedule('test.csv', 'Algoritmen en complexiteit')