from code.algorithms.heuristics_hillclimber import IncreasingMutationsClimber
from statistics import mean

import time
import matplotlib.pyplot as plt
import csv
import pandas as pd 
import os 


def increasing_mutations_all_averages(schedule, nr_climbers: int =10, nr_iterations: int =10):
    ''' 
    Writes a csv data file, storing the average, min, and max values of nr_climbers 
    per each of nr_iterations and for all types of maluspoints.   
    Stores thei final schedule of each climber in a separate folder. 
    '''

    # initialise results 
    results = []
    
    # if not existing, make separate folder to store schedules 
    dir_path = f'results/increasing_mutations/{nr_climbers}runs{nr_iterations}iters'
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # set number of runs
    for i in range(nr_climbers):
        
        # store results of each algorithm iteration 
        result = []
        
        # make a hillclimber object  
        climber = IncreasingMutationsClimber(schedule)

        print(f"Running Hill Climber Number: {i}")
        
        # set number iterations per run 
        for j in range(nr_iterations):
            
            # keep track of iterations 
            if j % 100 == 0:
                print(j)
            
            # run the algorithm for one iteration 
            climber.run(1)

            # store maluspoints for this iteration
            result.append((climber.maluspoints, 
                           climber.schedule.get_evening_room_maluspoints(),
                           climber.schedule.get_overcapacity_maluspoints(),
                           climber.schedule.get_student_maluspoints()[0],
                           climber.schedule.get_student_maluspoints()[1]))

        # store final schedules of each run  
        climber.schedule.get_output(dir_path+f'/increasing_mutations{i + 1}_output.csv')

        # append iteration maluspoints to all results 
        results.append(result)

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

    with open(f"results/increasing_mutations/increasing_mutations_climber_all_averages-{nr_climbers}-{nr_iterations}.csv", 'w', newline='') as output_file:
        result_writer = csv.writer(output_file, delimiter=',')
        #result_writer.writerow(["Mean Maluspoints", "Min Maluspoints", "Max Maluspoints"])
        
        for value in values:
            result_writer.writerow(value)


def increasing_mutations_ratios_plot(nr_climbers: int =10, nr_iterations: int =10):
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
    
    df = pd.read_csv(f'results/increasing_mutations/increasing_mutations_climber_all_averages-{nr_climbers}-{nr_iterations}.csv', names=names)
    
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
    plt.title(f'Maluspoints of n={nr_climbers} Increasing Mutations Hillclimbers')
    plt.ylabel('Average Maluspoints')
    plt.xlabel('Iterations')

    fig.savefig(f"results/increasing_mutations/increasing_mutations_climber_all_averages-{nr_climbers}-{nr_iterations}.png", dpi=1200)


def increasing_mutations_ratios_plot_zoom(nr_climbers: int =30, nr_iterations : int =20000, zoom_start : int =15000, zoom_end : int =20000):
    '''
    Zooms in to a specific range of hillclimber iterations.
    Plots the averages, min, and max values of all maluspoint types in that range.
    '''
    names = ['Total Avg', 'Total Min', 'Total Max', 
             'Evening Avg', 'Evening Min', 'Evening Max',
             'Overcap Avg', 'Overcap Min', 'Overcap Max', 
             'Free Avg', 'Free Min', 'Free Max',
             'Double Avg', 'Double Min', 'Double Max']
    
    df = pd.read_csv(f'results/increasing_mutations_climber/increasing_mutations_climber_all_averages-{nr_climbers}-{nr_iterations}.csv', names=names)
    
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
    plt.title(f'Maluspoints of n={nr_climbers} Increasing Mutations Hillclimbers')
    plt.ylabel('Average Maluspoints')
    plt.xlabel('Iterations')

    fig.savefig(f"results/increasing_mutations_climber/increasing_mutations_climber_all_averages_zoom-{nr_climbers}-{nr_iterations}.png", dpi=1200)





