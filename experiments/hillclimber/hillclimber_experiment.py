#from code.algorithms.hillclimber import Hillclimber
from statistics import mean
from scipy import stats

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

def timed_hillclimber_runs(schedule):
    """
    Runs hillclimber for 60 seconds and measures the time.
    Need to export results if we will use it. 
    """
    
    # add a seed for randomness 
    random.seed(123)

    # make a hillclimber object  
    climber = Hillclimber(schedule)
    
    start = time.time()
    n_runs = 0
    while time.time() - start < 60:
        print(f"run: {n_runs}")
        climber.run(1)
        n_runs += 1
    print(f'{n_runs} runs in 60 seconds')


def hillclimb(schedule, algorithm, name='Hillclimber', n_algorithms=30, n_iters=1000):
    """ 
    Runs hillclimber algorithm X times for Y iterations. 
    Returns csv file with final maluspoints at each run.   
    """

    print(f"Running {name}...")
    with open(f"results/hillclimber/{name}_iter{n_iters}.csv", 'w', newline='') as output_file:
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

def hillclimb_averages(schedule, nr_climbers, nr_iterations):
    
    # add a seed for randomness 
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
        values.append((mean(iteration), min(iteration), max(iteration)))

    with open("results/hillclimber/hillclimber_averages.csv", 'w', newline='') as output_file:
        result_writer = csv.writer(output_file, delimiter=',')
        #result_writer.writerow(["Mean Maluspoints", "Min Maluspoints", "Max Maluspoints"])
        
        for value in values:
            result_writer.writerow(value)


def hillclimber_averages_plot(nr_climbers, file_name="results/hillclimber/hillclimber_averages.csv"):
    """ 
    Makes a plot of the mean, min, and max number of maluspoints at each iteration.
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
    ax.set_title(f'Hillclimbers (n={nr_climbers}, iters/run={len(results)})')
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Average Maluspoints')
    fig.savefig("results/hillclimber/hillclimber_averages.png")


# make the plot for all types of maluspoints, not finalised yet  
def hillclimb_averages_all():
    """ 
    Makes a plot of the mean, min, and max number of maluspoints at each iteration for 
    each of the different types of maluspoints.
    Types of maluspoints: overcapacity, free period, evening slot, student double bookings.

    TODO: 
    - finalise
    - get all types of maluspoints in function and make csv of them. 
    - enable making a png file with same name as input 
    """ 
    # make plots for each of the separate types of maluspoints 
    hillclimber_averages_plot("results/hillclimber/hillclimber_averages_doublebookings.csv")
    hillclimber_averages_plot("results/hillclimber/hillclimber_averages_doublebookings.csv")





