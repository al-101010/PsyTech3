from code.algorithms.hillclimber import Hillclimber
from statistics import mean
from scipy import stats
from functools import reduce

import time
import matplotlib.pyplot as plt
import random 
import csv
import pandas as pd 

"""
TODOs:
- Note: fixing same axis for plot not necessary if always same seed! 
- finalise plot different types of maluspoints 
"""

def hillclimb(schedule, algorithm, name='Hillclimber', n_algorithms=30, n_iters=1000):
    """ 
    Runs hillclimber algorithm X times for Y iterations. 
    Returns csv file (algorithm name, number of runs, number of iters/run) with final maluspoints at each run.   
    """

    print(f"Running {name}...")
    with open(f"results/hillclimber/{name}{n_algorithms}_iter{n_iters}.csv", 'w', newline='') as output_file:
        result_writer = csv.writer(output_file, delimiter=',')

        for i in range(n_algorithms):
            print(f'running algorithm nr: {i}')
            
            # add a seed for randomness 
            random.seed(123)

            # make and run a hillclimber object  
            climber = algorithm(schedule)
            climber.run(n_iters)

            # get all maluspoints and different types of maluspoints at each run 
            all_maluspoints = [climber.schedule.get_total_maluspoints(),
                                climber.schedule.get_evening_room_maluspoints(),
                                climber.schedule.get_overcapacity_maluspoints(),
                                climber.schedule.get_student_maluspoints()[0],
                                climber.schedule.get_student_maluspoints()[1]]
            
            # write results into csv file 
            result_writer.writerow(all_maluspoints)


def compare_hillclimbers(hillclimber1_data, hillclimber2_data):
    """ 
    Compares the results of two hillclimbers with different functionalities with a t-test. 
    Returns their means in order of entry into the function, t-statistic, and p-value. 
    """

    # read in data and make df 
    names = ['Total', 'Evening Room', 'Overcapacity', 'Free Period', 'Double Booking']
    hillclimber1_results = pd.read_csv(hillclimber1_data, names=names)
    hillclimber2_results = pd.read_csv(hillclimber2_data, names=names)

    hillclimber1_mean = mean(hillclimber1_results['Total'])
    hillclimber2_mean = mean(hillclimber2_results['Total'])
    
    t_stat, p_val = stats.ttest_ind(hillclimber1_results['Total'], hillclimber2_results['Total'])

    print(f'mean 1: {hillclimber1_mean}\nmean 2: {hillclimber2_mean}\nT-statistic: {t_stat}\nP-value: {p_val}')
    if p_val < 0.05:
        print('this difference is significant')
    
    return hillclimber1_mean, hillclimber2_mean, t_stat, p_val


def hillclimb_all_averages(schedule, nr_climbers, nr_iterations):
    ''' 
    Writes a csv storing the average, min, and max values of nr_climbers per each of 
    nr_iterations for all types of maluspoints.   
    '''
    # add a seed 
    random.seed(123)

    # initialise results 
    results = []
    
    # define how many hillclimbers you want to run 
    for i in range(nr_climbers):
        
        # store results of each algorithm run 
        result = []
        
        # make a hillclimber object  
        climber = Hillclimber(schedule)
        
        print(f"Running Hill Climber Number: {i}")
        # run the algorithm X times 
        for j in range(nr_iterations):
            
            # run the algorithm for one iteration 
            climber.run(1)

            # append maluspoints for this iteration to results
            result.append((climber.schedule.get_total_maluspoints(), 
                           climber.schedule.get_evening_room_maluspoints(),
                           climber.schedule.get_overcapacity_maluspoints(),
                           climber.schedule.get_student_maluspoints()[0],
                           climber.schedule.get_student_maluspoints()[1]))
            # result.append(climber.schedule.get_total_maluspoints())

        # append result to all results 
        results.append(result)

    # get all values for a row 
    values = []
    for iteration in zip(*results):
        
        iteration = list(zip(*list(iteration)))
        
        # values.append(mean(iteration[0]), min(iteration[0]), max(iteration[0]))
        values.append((mean(iteration[0]), min(iteration[0]), max(iteration[0]),
                       mean(iteration[1]), min(iteration[1]), max(iteration[1]),
                       mean(iteration[2]), min(iteration[2]), max(iteration[2]),
                       mean(iteration[3]), min(iteration[3]), max(iteration[3]),
                       mean(iteration[4]), min(iteration[4]), max(iteration[4])))

    with open("results/hillclimber/hillclimber_all_averages.csv", 'w', newline='') as output_file:
        result_writer = csv.writer(output_file, delimiter=',')
        #result_writer.writerow(["Mean Maluspoints", "Min Maluspoints", "Max Maluspoints"])
        
        for value in values:
            result_writer.writerow(value)


def hillclimber_ratios_plot_zoom(runs=10, zoom_start=80, zoom_end=100):
    '''
    Zooms in to a specific range of hillclimber iterations.
    Plots the averages, min, and max values of all maluspoint types in that range.
    '''
    names = ['Total Avg', 'Total Min', 'Total Max', 
             'Evening Avg', 'Evening Min', 'Evening Max',
             'Overcap Avg', 'Overcap Min', 'Overcap Max', 
             'Free Avg', 'Free Min', 'Free Max',
             'Double Avg', 'Double Min', 'Double Max']
    
    df = pd.read_csv('results/hillclimber/hillclimber_all_averages.csv', names=names)
    
    # df = df.iloc[zoom_start:zoom_end]
    df = df.iloc[zoom_start:zoom_end]

    fig, ax = plt.subplots()

    # plot the lines for all maluspoints 
    ax.plot(df['Total Avg'])
    ax.plot(df['Evening Avg'])
    ax.plot(df['Overcap Avg'])
    ax.plot(df['Free Avg'])
    ax.plot(df['Double Avg'])

    # plot min and max for all maluspoints 
    zoom_range = [zoom_start, zoom_end]
    ax.fill_between(range(*zoom_range), df['Total Min'], df['Total Max'], alpha = 0.2)
    ax.fill_between(range(*zoom_range), df['Evening Min'], df['Evening Max'], alpha = 0.2)
    ax.fill_between(range(*zoom_range), df['Overcap Min'], df['Overcap Max'], alpha = 0.2)
    ax.fill_between(range(*zoom_range), df['Free Min'], df['Free Max'], alpha = 0.2)
    ax.fill_between(range(*zoom_range), df['Double Min'], df['Double Max'], alpha = 0.2)

    # set y axis same for all plots      
    ax.set_ybound(0, 300)

    plt.legend(['Total', 'Evening Room', 'Overcapacity', 'Free Period', 'Double Booking'])
    plt.title(f'Maluspoints of n={runs} Hillclimbers.')
    plt.ylabel('Average Maluspoints')
    plt.xlabel('Iterations')

    fig.savefig("results/hillclimber/hillclimber_all_averages_zoom.png", dpi=1200)


def hillclimber_ratios_plot(runs=10, iters=100):
    '''
    Plots the averages, min, and max values of all maluspoint types for an algorithm 
    for a certain amount of runs.  
    '''
    names = ['Total Avg', 'Total Min', 'Total Max', 
             'Evening Avg', 'Evening Min', 'Evening Max',
             'Overcap Avg', 'Overcap Min', 'Overcap Max', 
             'Free Avg', 'Free Min', 'Free Max',
             'Double Avg', 'Double Min', 'Double Max']
    
    df = pd.read_csv('results/hillclimber/hillclimber_all_averages.csv', names=names)
    
    fig, ax = plt.subplots()

    # plot the lines for all maluspoints 
    ax.plot(df['Total Avg'])
    ax.plot(df['Evening Avg'])
    ax.plot(df['Overcap Avg'])
    ax.plot(df['Free Avg'])
    ax.plot(df['Double Avg'])

    # plot min and max for all maluspoints 
    ax.fill_between(range(iters), df['Total Min'], df['Total Max'], alpha = 0.2)
    ax.fill_between(range(iters), df['Evening Min'], df['Evening Max'], alpha = 0.2)
    ax.fill_between(range(iters), df['Overcap Min'], df['Overcap Max'], alpha = 0.2)
    ax.fill_between(range(iters), df['Free Min'], df['Free Max'], alpha = 0.2)
    ax.fill_between(range(iters), df['Double Min'], df['Double Max'], alpha = 0.2)
    
    # set y axis same for all plots      
    ax.set_ybound(0, 2500)

    plt.legend(['Total', 'Evening Room', 'Overcapacity', 'Free Period', 'Double Booking'])
    plt.title(f'Maluspoints of n={runs} Hillclimbers')
    plt.ylabel('Average Maluspoints')
    plt.xlabel('Iterations')

    fig.savefig("results/hillclimber/hillclimber_all_averages.png", dpi=1200)


""" NOT SURE IF WILL USE"""
def timed_hillclimber_runs(schedule, algorithm):
    """
    Runs hillclimber for 60 seconds and measures the time.
    Need to export results if we will use it. 
    """
    
    # add a seed for randomness 
    random.seed(123)

    # make a hillclimber object  
    climber = algorithm(schedule)
    
    start = time.time()
    n_runs = 0
    while time.time() - start < 60:
        print(f"run: {n_runs}")
        climber.run(1)
        n_runs += 1
    print(f'{n_runs} runs in 60 seconds')


"""DEPRECATED"""
def hillclimb_averages(schedule, nr_climbers, nr_iterations):
    """
    Gets the average, min, max of each hillclimber runs. 
    Replaced by hillclimb all averages. 
    TODO: check if still needed, remove 
    """
    # add a seed 
    random.seed(123)

    # initialise results 
    results = []
    
    # define how many hillclimbers you want to run 
    for i in range(nr_climbers):
        
        # store results of each algorithm run 
        result = []
        
        # make a hillclimber object  
        climber = Hillclimber(schedule)
        
        print(f"Running Hill Climber Number: {i}")
        # run the algorithm X times 
        for j in range(nr_iterations):
            
            # run the algorithm for one iteration 
            climber.run(1)

            # append maluspoints for this iteration to results
            result.append(climber.schedule.get_total_maluspoints())

        # append result to all results 
        results.append(result)

    # get all values for a row 
    values = []
    for iteration in zip(*results):
        
        iteration = list(zip(*list(iteration)))
        
        values.append(mean(iteration[0]), min(iteration[0]), max(iteration[0]))

    with open("results/hillclimber/hillclimber_averages.csv", 'w', newline='') as output_file:
        result_writer = csv.writer(output_file, delimiter=',')
        #result_writer.writerow(["Mean Maluspoints", "Min Maluspoints", "Max Maluspoints"])
        
        for value in values:
            result_writer.writerow(value)

def hillclimber_averages_plot(nr_climbers, file_name="results/hillclimber/hillclimber_averages.csv"):
    """ 
    Replaced by hillclimber ratios plot. 
    Makes a plot of the mean, min, and max number of maluspoints at each iteration.
    TODO: check if still needed, remove 
    """
    fig, ax = plt.subplots()
    with open(file_name, 'r') as input_file:
        result_reader = csv.reader(input_file, delimiter=',')
        results = [(float(average), int(minimum), int(maximum)) for average, minimum, maximum in result_reader]
        averages = [average for average, minimum, maximum in results]
        minima = [minimum for average, minimum, maximum in results]
        maxima = [maximum for average, minimum, maximum in results]

    ax.plot(averages, label='Hillclimber')
    ax.fill_between(range(0, len(averages)), minima, maxima, alpha=0.5, linewidth=0)
    ax.set_title(f'Hillclimbers (n={nr_climbers})')
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Average Maluspoints')
    fig.savefig("results/hillclimber/hillclimber_averages.png")





