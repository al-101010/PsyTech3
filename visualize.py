import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tabulate
from tabulate import tabulate as tabulate_data

def print_timetable_for_student(timetable_file: str, student_name: str) -> None:
    """
    Function that takes a csv file containing all scheduling information, as well
    as the full name of a student, and prints their weekly schedule
    """
    # initialize variables
    timeslots = [9, 11, 13, 15, 17]
    days = ['ma', 'di', 'wo', 'do', 'vr']

    # load in data
    timetable_df = pd.read_csv(timetable_file)

    # filter for student
    student_df = timetable_df[timetable_df['Student'] == student_name]

    # add series containing all relevant info
    student_df['alle_info'] = student_df['Vak'] + ' - ' + student_df['Activiteit'] + ' - ' + student_df['Zaal']

    # reorganize table / df
    schedule = pd.pivot_table(student_df, values='alle_info', index='Tijdslot', columns='Dag', aggfunc=lambda x: '\n'.join(x))
    schedule = schedule.reindex(index=timeslots, columns=days)
    schedule.fillna('', inplace=True)

    # create table 
    # TO DO: Layout fixen zodat timetable altijd op scherm past OF afkortingen van vakken gebruiken
    tabulated_schedule = tabulate_data(schedule, headers='keys', tablefmt='fancy_grid', showindex='always')
    
    print(f"Weekrooster voor {student_name}:\n")
    print(tabulated_schedule)

def obtain_course_schedule(timetable_file: str, course_name: str) -> None:
    """
    Function that takes a csv file containing all scheduling information, as well as a 
    string containing the name of a course, and prints the weekly schedule for said
    course
    """
    # initialize variables
    timeslots = [9, 11, 13, 15, 17]
    days = ['ma', 'di', 'wo', 'do', 'vr']

    # load in data
    df = pd.read_csv(timetable_file)

    # filter by course
    course_df = df.groupby('Vak').get_group(course_name)

    # add series containing all relevant info 
    course_df['alle_info'] = course_df['Activiteit'] + ' - ' + course_df['Zaal']

    course_schedule = pd.pivot_table(course_df, values='alle_info', index='Tijdslot', columns='Dag', aggfunc=lambda x: '\n'.join(set(x)))
    course_schedule = course_schedule.reindex(index=timeslots, columns=days)
    course_schedule.fillna('', inplace=True)

    table = tabulate_data(course_schedule, headers='keys', tablefmt='fancy_grid', showindex='always')

    print(f"Weekrooster voor {course_name} \n")
    print(table)

def show_activity_heatmap(timetable_file: str, save: bool = False, output_file: str = None) -> None:
    """
    Function that plots the number of unique activities scheduled per timeslot, using a heatmap
    """
    # initialize variables
    timeslots = [9, 11, 13, 15, 17]
    days = ['ma', 'di', 'wo', 'do', 'vr']

    # load data 
    df = pd.read_csv(timetable_file)
    df['alle_info'] = df['Vak'] + ' - ' + df['Activiteit'] + ' - ' + df['Zaal']

    unique_activity_count = pd.pivot_table(df, index='Tijdslot', columns='Dag', values='alle_info', aggfunc=pd.Series.nunique, fill_value=0)
    unique_activity_count = unique_activity_count.reindex(index=timeslots, columns=days)

    # plot heatmap: higher value darker
    plt.figure(figsize=(8, 6))
    sns.heatmap(unique_activity_count, annot=True, cmap=sns.cubehelix_palette(as_cmap=True), linewidths=.5, linecolor='k')
    plt.title("Unieke Activiteiten per Tijdslot")
    plt.xlabel("Dag")
    plt.ylabel("Tijdslot")
    plt.yticks(rotation=0)
    
    if save:
        plt.savefig(output_file)

    plt.show()



print_timetable_for_student('LecturesLesroosters/test_output.csv', 'Yanick Abbing')
obtain_course_schedule('LecturesLesroosters/test_output.csv', 'Software engineering')
show_activity_heatmap('LecturesLesroosters/test_output.csv')