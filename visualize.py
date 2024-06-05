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
    student_df = timetable_df[timetable_df['Student'] == student_name]
    student_df['alle_info'] = student_df['Vak'] + ' - ' + student_df['Activiteit'] + ' - ' + student_df['Zaal']

    schedule = pd.pivot_table(student_df, values='alle_info', index='Tijdslot', columns='Dag', aggfunc=lambda x: '\n'.join(x))
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

    course_df = df.groupby('Vak').get_group(course_name)
    course_df['alle_info'] = course_df['Activiteit'] + ' - ' + course_df['Zaal']

    course_schedule = pd.pivot_table(course_df, values='alle_info', index='Tijdslot', columns='Dag', aggfunc=lambda x: '\n'.join(set(x)))
    course_schedule = course_schedule.reindex(index=timeslots, columns=days)
    course_schedule.fillna('', inplace=True)

    table = tabulate_data(course_schedule, headers='keys', tablefmt='fancy_grid', showindex='always')

    print(f"Weekrooster voor {course_name} \n")
    print(table)


print_timetable_for_student('test_output.csv', 'Yanick Abbing')
obtain_course_schedule('test_output.csv', 'Software engineering')