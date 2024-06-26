import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tabulate
from tabulate import tabulate as tabulate_data
import textwrap

def wrap_text(text: str, width: int = 35) -> str:
    """
    Function that takes a text and wraps it within the specified width
    """
    wrapped_lines = []
    
    for line in text.split('\n'):
        wrapped_lines.append(textwrap.fill(line, width))
    
    return '\n'.join(wrapped_lines)
    
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

    # wrap text
    for column in schedule.columns:
        schedule[column] = schedule[column].apply(lambda x: wrap_text(x))
        
    # create table 
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

    # wrap text
    for column in course_schedule.columns:
        course_schedule[column] = course_schedule[column].apply(lambda x: wrap_text(x))
    
    table = tabulate_data(course_schedule, headers='keys', tablefmt='fancy_grid', showindex='always')

    print(f"Weekrooster voor {course_name} \n")
    print(table)

def obtain_room_schedule(timetable_file: str, room_id: str) -> None:
    """
    Function that takes a csv file containing all scheduling information, as well as a 
    string containing a room id, and prints the weekly schedule for said room
    """

    # initialize variables
    timeslots = [9, 11, 13, 15, 17]
    days = ['ma', 'di', 'wo', 'do', 'vr']

    # load in data
    df = pd.read_csv(timetable_file)

    room_df = df.groupby('Zaal').get_group(room_id)
    room_df['alle_info'] = room_df['Vak'] + ' - ' + room_df['Activiteit']

    room_schedule = pd.pivot_table(room_df, values='alle_info', index='Tijdslot', columns='Dag', aggfunc=lambda x: '\n'.join(set(x)))
    room_schedule = room_schedule.reindex(index=timeslots, columns=days)
    room_schedule.fillna('', inplace=True)

    # wrap text
    for column in room_schedule.columns:
        room_schedule[column] = room_schedule[column].apply(lambda x: wrap_text(x))

    table = tabulate_data(room_schedule, headers='keys', tablefmt='fancy_grid', showindex='always')

    print(f"Weekrooster voor zaal {room_id} \n")
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
    sns.heatmap(unique_activity_count, annot=True, cmap=sns.cubehelix_palette(as_cmap=True), linewidths=.5, linecolor='k')
    plt.title("Unieke Activiteiten per Tijdslot")
    plt.xlabel("Dag")
    plt.ylabel("Tijdslot")
    plt.yticks(rotation=0)
    
    if save and output_file:
        plt.savefig(output_file)
    
    plt.show()



print_timetable_for_student('../data/random_output.csv', 'Rhona Vromans')
obtain_course_schedule('../data/random_output.csv', 'Software engineering')
show_activity_heatmap('../data/random_output.csv')
obtain_room_schedule('../data/random_output.csv', 'C0.110')