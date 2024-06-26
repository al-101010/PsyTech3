import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tabulate
from tabulate import tabulate as tabulate_data
import textwrap
import argparse

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

    # print error if student not in data file
    if not student_name in timetable_df['Student'].values:
        raise Exception(f"{student_name} is not present in your data")
    
    # filter for student
    student_df = timetable_df[timetable_df['Student'] == student_name].copy()

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

    # print error if course not in data file
    if not course_name in df['Vak'].values:
        raise Exception(f"{course_name} is not present in your data")

    # filter by course
    course_df = df.groupby('Vak').get_group(course_name).copy()

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

    # print error if room not in data file
    if not room_id in df['Zaal'].values:
        raise Exception(f"{room_id} is not present in your data")

    # filter by room
    room_df = df.groupby('Zaal').get_group(room_id).copy()
    
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

def main(schedule_type, name, schedule_csv):
    if schedule_type == 'student':
        print_timetable_for_student(schedule_csv, name)
    elif schedule_type == 'course':
        obtain_course_schedule(schedule_csv, name)
    elif schedule_type == 'room':
        obtain_room_schedule(schedule_csv, name)
    else:
        show_activity_heatmap(schedule_csv)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "create visualization of a schedule")

    # Adding arguments
    parser.add_argument("schedule_type", help = "desired type of schedule")
    parser.add_argument("name", help = "name of the subject of desired schedule")
    parser.add_argument("-s", "--schedule_csv", default='../../results/hillclimber/tested_hillclimber_output_500K.csv', help = "file path that holds schedule output to be visualized")

    # Read arguments from command line
    args = parser.parse_args()
    main(args.schedule_type, args.name, args.schedule_csv)
