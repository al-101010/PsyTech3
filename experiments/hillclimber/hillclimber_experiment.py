from code.algorithms.hillclimber import Hillclimber
from code.algorithms.heuristics_hillclimber import MutationProbabilityClimber, ProblematicActivityClimber, ProblematicStudentsClimber, IncreasingMutationsClimber
from statistics import mean
from scipy import stats
from code.classes.schedule import Schedule

import time
import matplotlib.pyplot as plt
import random 
import csv
import pandas as pd 
import os 
import seaborn as sns

def select_version(schedule, version):
    """
    Selects a version of a hillclimber algorithm and makes a schedule based on selection.
    """

    if version == 'hillclimber':
        algorithm = Hillclimber(schedule)
    elif version == 'problematic_students':
        algorithm = ProblematicStudentsClimber(schedule)
    elif version == 'problematic_activity':
        algorithm = ProblematicActivityClimber(schedule)
    elif version == 'mutation_probability':
        algorithm = MutationProbabilityClimber(schedule)
    elif version == 'increasing_mutations':
        algorithm = IncreasingMutationsClimber(schedule)
    
    return algorithm

def hillclimb_all_averages(schedule, version, nr_climbers: int =30, nr_iterations: int =20000):
    ''' 
    Writes a csv data file, storing the average, min, and max values of nr_climbers 
    per each of nr_iterations and for all types of maluspoints.   
    Stores thei final schedule of each climber in a separate folder. 
    '''
    start_time = time.time()

    # initialise results 
    results = []

    # initialise maluspoints collector per run 
    maluspoints = []

    # select version 
    algorithm = select_version(schedule, version)
    
    # if not existing, make separate folder to store schedules 
    dir_path = f'results/{version}/{nr_climbers}runs{nr_iterations}iters'
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # set number of runs
    for i in range(nr_climbers):
        
        # store results of each algorithm iteration 
        result = []
        
        # make a hillclimber object  
        climber = algorithm

        print(f"Running Hill Climber Number: {i}")
        
        # set number iterations per run 
        for j in range(nr_iterations):
            
            # keep track of iterations 
            if j % 100 == 0:
                print(j)
            
            # run the algorithm for one iteration 
            climber.run(1)

            evening = climber.schedule.get_evening_room_maluspoints()
            overcapacity = climber.schedule.get_overcapacity_maluspoints()
            free_period =  climber.schedule.get_student_maluspoints()[0]
            double_booking = climber.schedule.get_student_maluspoints()[1]
            total = double_booking + overcapacity + evening + free_period

            # store maluspoints for this iteration
            result.append((total, evening, overcapacity, free_period, double_booking))

        # store final maluspoints of this run separately 
        maluspoints.append(total)

        # store final schedules of each run  
        climber.schedule.get_output(dir_path+f'/{version}{i + 1}_output.csv')

        # append iteration maluspoints to all results 
        results.append(result)
 
    # store final maluspoints in separate file  
    maluspoints = pd.DataFrame(maluspoints, columns=['Final Maluspoints'])
    maluspoints.to_csv(dir_path+'/final_maluspoints.csv')

    # get all values for a row 
    values = []

    # loop over zipped results 
    for iteration in zip(*results):
        
        # unzip to get the same type maluspoints in one row 
        iteration = list(zip(*list(iteration)))
        
        # append average, mean, and max of each type of maluspoints to values 
        values.append((mean(iteration[0]), min(iteration[0]), max(iteration[0]),
                       mean(iteration[1]), min(iteration[1]), max(iteration[1]),
                       mean(iteration[2]), min(iteration[2]), max(iteration[2]),
                       mean(iteration[3]), min(iteration[3]), max(iteration[3]),
                       mean(iteration[4]), min(iteration[4]), max(iteration[4])))

    with open(f"results/{version}/{version}_all_averages-{nr_climbers}-{nr_iterations}.csv", 'w', newline='') as output_file:
        result_writer = csv.writer(output_file, delimiter=',')
        #result_writer.writerow(["Mean Maluspoints", "Min Maluspoints", "Max Maluspoints"])
        
        for value in values:
            result_writer.writerow(value)
    
    end_time = time.time()
    
    print(f'--- {round(end_time - start_time, 1)} seconds ---')


def hillclimber_ratios_plot(version, nr_climbers: int =30, nr_iterations: int =20000):
    '''
    Plots the averages, min, and max values of the maluspoint types of nr_climbers 
    per iteration in nr_iterations.
    '''

    # read in data file 
    names = ['Total Avg', 'Total Min', 'Total Max', 
             'Evening Avg', 'Evening Min', 'Evening Max',
             'Overcap Avg', 'Overcap Min', 'Overcap Max', 
             'Free Avg', 'Free Min', 'Free Max',
             'Double Avg', 'Double Min', 'Double Max']
    
    df = pd.read_csv(f'results/{version}/{version}_all_averages-{nr_climbers}-{nr_iterations}.csv', names=names)
    
    fig, ax = plt.subplots()

    # plot the lines for all maluspoints 
    ax.plot(df['Total Avg'])
    ax.plot(df['Evening Avg'])
    ax.plot(df['Overcap Avg'])
    ax.plot(df['Free Avg'])
    ax.plot(df['Double Avg'])

    # plot min and max for all maluspoints 
    ax.fill_between(range(nr_iterations), df['Total Min'], df['Total Max'], alpha = 0.2)
    ax.fill_between(range(nr_iterations), df['Evening Min'], df['Evening Max'], alpha = 0.2)
    ax.fill_between(range(nr_iterations), df['Overcap Min'], df['Overcap Max'], alpha = 0.2)
    ax.fill_between(range(nr_iterations), df['Free Min'], df['Free Max'], alpha = 0.2)
    ax.fill_between(range(nr_iterations), df['Double Min'], df['Double Max'], alpha = 0.2)
    
    # set y axis, range 0 to 1500 works best        
    ax.set_ybound(0, 1500)

    plt.legend(['Total', 'Evening Room', 'Overcapacity', 'Free Period', 'Double Booking'], loc='upper right')
    plt.suptitle(f'Maluspoints Hillclimber (n={nr_climbers})', fontsize=12)
    plt.title(f'final maluspoints obtained - average: {df["Total Avg"].iloc[-1]}, minimum: {df["Total Min"].iloc[-1]}, maximum: {df["Total Max"].iloc[-1]}', loc='left', fontsize=9)
    plt.ylabel('Average Maluspoints')
    plt.xlabel('Iterations')

    fig.savefig(f"results/{version}/{version}_all_averages-{nr_climbers}-{nr_iterations}.png", dpi=1200)
    plt.show()

def hillclimber_ratios_plot_zoom(version, nr_climbers: int =30, nr_iterations : int =20000, zoom_start : int =15000, zoom_end : int =20000):
    '''
    Zooms in to a specific range of hillclimber iterations.
    Plots the averages, min, and max values of all maluspoint types in that range.
    '''
    names = ['Total Avg', 'Total Min', 'Total Max', 
             'Evening Avg', 'Evening Min', 'Evening Max',
             'Overcap Avg', 'Overcap Min', 'Overcap Max', 
             'Free Avg', 'Free Min', 'Free Max',
             'Double Avg', 'Double Min', 'Double Max']
    
    df = pd.read_csv(f'results/{version}/{version}_all_averages-{nr_climbers}-{nr_iterations}.csv', names=names)
    
    # make subset of data to zoom in to
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

    # set y axis, 0 to 300 works best for this range of iterations      
    ax.set_ybound(0, 300)

    plt.legend(['Total', 'Evening Room', 'Overcapacity', 'Free Period', 'Double Booking'])
    plt.suptitle(f'Maluspoints Hillclimber (n={nr_climbers})', fontsize=12)
    plt.title(f'final maluspoints obtained - average: {df["Total Avg"].iloc[-1]}, minimum: {df["Total Min"].iloc[-1]}, maximum: {df["Total Max"].iloc[-1]}', loc='left', fontsize=9)
    plt.ylabel('Average Maluspoints')
    plt.xlabel('Iterations')

    fig.savefig(f"results/{version}/{version}_all_averages_zoom-{nr_climbers}-{nr_iterations}.png", dpi=1200)
    plt.show()

def plot_maluspoints_distribution(version, nr_climbers=30, nr_iterations=20000):
    """
    Plots a histogram of the distribution of maluspoints in N schedules.  
    """

    maluspoints_df = pd.read_csv(f'results/{version}/{nr_climbers}runs{nr_iterations}iters/final_maluspoints.csv')

    maluspoints = maluspoints_df['Final Maluspoints'].to_list()
    
    fig, ax = plt.subplots()
    
    sns.histplot(maluspoints, bins=6, kde=True, edgecolor='black')
    plt.xlabel('Number Maluspoints')
    plt.ylabel('Number Generated Schedules')
    plt.title(f'Maluspoints Distribution {version} (n={nr_climbers})')
    plt.savefig(f'results/{version}/final_maluspoints-{nr_climbers}-{nr_iterations}.png', dpi=1200)
    plt.show()


""" NOT SURE IF WILL USE"""
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


def timed_hillclimber_runs(schedule, algorithm):
    """
    Runs hillclimber for 60 seconds and measures the number of iterations.
    TODO: Need to export results if we will use it?
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



