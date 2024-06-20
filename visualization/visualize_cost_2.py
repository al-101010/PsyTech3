import matplotlib.pyplot as plt
import seaborn as sns
import random
import pandas as pd

from code.classes.schedule import Schedule
from code.algorithms.random_alg import Random

def run_algorithm(algorithm, schedule, iterations):
    maluspoints_total = []
    maluspoints_double_booking = []
    maluspoints_free_period = []
    maluspoints_overcapacity = []
    maluspoints_evening_room = []


    for i in range(iterations):
        print(i)
        random_schedule = algorithm(schedule)
        maluspoints_total.append(random_schedule.schedule.get_total_maluspoints())
        
        free_period, double_booking = random_schedule.schedule.get_student_maluspoints()
        
        maluspoints_double_booking.append(double_booking)
        maluspoints_free_period.append(free_period)
        maluspoints_overcapacity.append(random_schedule.schedule.get_overcapacity_maluspoints())
        maluspoints_evening_room.append(random_schedule.schedule.get_evening_room_maluspoints())


    return maluspoints_total, maluspoints_double_booking, maluspoints_free_period, maluspoints_overcapacity, maluspoints_evening_room

def visualize_maluspoints_barplot(algorithm, schedule, iterations):
    # get all types of maluspoints  
    maluspoints_total, maluspoints_double_booking, maluspoints_free_period, maluspoints_overcapacity, maluspoints_evening_room = run_algorithm(algorithm, schedule, iterations)
    
    # make data frame from maluspoints, !!! evening room not included for now because too small distribution !!!
    maluspoints_dict = {'free_period': maluspoints_free_period, 'double_booking':maluspoints_double_booking, 
                        'overcapacity': maluspoints_overcapacity}
    
    # make data frame 
    df = pd.DataFrame(maluspoints_dict)
    
    # make plot for different types 
    sns.histplot(df, bins=50, kde=True, edgecolor='black')
    plt.xlabel('Number Maluspoints')
    plt.ylabel('Number Generated Schedules')
    plt.title('Distribution of maluspoints per type (evening room excluded)')
    #plt.savefig('../data/cost_maluspoint_types.png')
    plt.show()

    # make plot for total 
    sns.histplot(maluspoints_total, bins=50, kde=True, edgecolor='black')
    plt.xlabel('Number Maluspoints')
    plt.ylabel('Number Generated Schedules')
    plt.title('Distribution of maluspoints over randomly generated schedules')
    #plt.savefig('../data/random_cost.png')
    plt.show()


schedule = Schedule('data/studenten_en_vakken.csv', 'data/vakken.csv', 'data/zalen.csv')
visualize_maluspoints_barplot(Random, schedule, 1000)
