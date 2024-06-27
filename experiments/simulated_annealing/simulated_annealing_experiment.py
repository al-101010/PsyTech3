from code.algorithms.simulated_annealing import SimulatedAnnealing
from statistics import mean

import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns 
import time 
import os 
import csv


def write_file(results, nr_algorithms, nr_iterations):
    '''
    Writes a csv file from results. 
    '''

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

    with open(f"results/simulated_annealing/simulated_annealing_all_averages-{nr_algorithms}-{nr_iterations}.csv", 'w', newline='') as output_file:
        result_writer = csv.writer(output_file, delimiter=',')
        
        for value in values:
            result_writer.writerow(value)

def simal_all_averages(schedule, nr_simal: int =30, nr_iterations: int =20000, temp: int =50):
    ''' 
    Writes a csv data file, storing the average, min, and max values of nr_simal 
    per each of nr_iterations and for all types of maluspoints.   
    Stores thei final schedule of each simulated annealing algorithm in a separate folder. 
    '''
    start_time = time.time()

    # initialise results 
    results = []

    # initialise maluspoints collector per run 
    maluspoints = []
    
    # if not existing, make separate folder to store schedules 
    dir_path = f'results/simulated_annealing/{nr_simal}runs{nr_iterations}iters'
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # set number of runs
    for i in range(nr_simal):
        
        # store results of each algorithm iteration 
        result = []
        
        # make a simulated annealing object  
        simal = SimulatedAnnealing(schedule, temp, cooling_function='exponential')
        
        print(f"Running Simulated Annealing Number: {i}")
        
        # set number iterations per run 
        for j in range(nr_iterations):
            
            # keep track of iterations 
            if j % 100 == 0:
                print(j)
            
            # run the algorithm for one iteration 
            simal.run(1)
                        
            evening = simal.schedule.get_evening_room_maluspoints()
            overcapacity = simal.schedule.get_overcapacity_maluspoints()
            free_period =  simal.schedule.get_student_maluspoints()[0]
            double_booking = simal.schedule.get_student_maluspoints()[1]
            total = double_booking + overcapacity + evening + free_period

            # store maluspoints for this iteration
            result.append((total, evening, overcapacity, free_period, double_booking))

        # store final maluspoints of this run separately 
        print(f'final maluspoints for this run {total}')
        maluspoints.append(total)

        # store final schedules of each run  
        simal.schedule.get_output(dir_path+f'/simulated_annealing{i + 1}_output.csv')

        # append iteration maluspoints to all results 
        results.append(result)

    # store final maluspoints in separate file  
    maluspoints = pd.DataFrame(maluspoints, columns=['Final Maluspoints'])
    maluspoints.to_csv(dir_path+'/final_maluspoints.csv')

    write_file(results, nr_simal, nr_iterations)
    
    end_time = time.time()
    print(f'--- {round(end_time - start_time, 1)} seconds ---')


def simal_all_averages_plot(nr_simal: int =30, nr_iterations: int =20000):
    '''
    Plots the averages, min, and max values of the maluspoint types of nr_simal 
    per iteration in nr_iterations.
    '''

    # read in data file 
    names = ['Total Avg', 'Total Min', 'Total Max', 
             'Evening Avg', 'Evening Min', 'Evening Max',
             'Overcap Avg', 'Overcap Min', 'Overcap Max', 
             'Free Avg', 'Free Min', 'Free Max',
             'Double Avg', 'Double Min', 'Double Max']
    
    df = pd.read_csv(f'results/simulated_annealing/simulated_annealing_all_averages-{nr_simal}-{nr_iterations}.csv', names=names)
    
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
    plt.suptitle(f'Maluspoints Simulated Annealing (n={nr_simal})', fontsize=12)
    plt.title(f'maluspoints avg: {round(df["Total Avg"].iloc[-1], 1)}, min: {round(df["Total Min"].iloc[-1], 1)}, max: {round(df["Total Max"].iloc[-1], 1)}', loc='left', fontsize=9)
    plt.title('temp: 50', loc='right', fontsize=9)
    plt.ylabel('Average Maluspoints')
    plt.xlabel('Iterations')

    fig.savefig(f"results/simulated_annealing/simulated_annealing_all_averages-{nr_simal}-{nr_iterations}.png", dpi=1200)
    plt.show()

def simal_all_averages_plot_zoom(nr_simal: int =30, nr_iterations : int =20000, zoom_start : int =15000, zoom_end : int =20000):
    '''
    Zooms in to a specific range of simulated annealing iterations.
    Plots the averages, min, and max values of all maluspoint types in that range.
    '''
    names = ['Total Avg', 'Total Min', 'Total Max', 
             'Evening Avg', 'Evening Min', 'Evening Max',
             'Overcap Avg', 'Overcap Min', 'Overcap Max', 
             'Free Avg', 'Free Min', 'Free Max',
             'Double Avg', 'Double Min', 'Double Max']
    
    df = pd.read_csv(f'results/simulated_annealing/simulated_annealing_all_averages-{nr_simal}-{nr_iterations}.csv', names=names)
    
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
    plt.suptitle(f'Maluspoints Simulated Annealing (n={nr_simal})', fontsize=12)
    plt.title(f'maluspoints avg: {round(df["Total Avg"].iloc[-1], 1)}, min: {round(df["Total Min"].iloc[-1], 1)}, max: {round(df["Total Max"].iloc[-1], 1)}', loc='left', fontsize=9)
    plt.title('temp: 50', loc='right', fontsize=9)
    plt.ylabel('Average Maluspoints')
    plt.xlabel('Iterations')

    fig.savefig(f"results/simulated_annealing/simulated_annealing_all_averages_zoom-{nr_simal}-{nr_iterations}.png", dpi=1200)
    plt.show()

def plot_maluspoints_distribution(nr_simal=30, nr_iterations=20000):
    """
    Plots a histogram of the distribution of maluspoints in N schedules.  
    """

    fig, ax = plt.subplots()

    maluspoints_df = pd.read_csv(f'results/simulated_annealing/{nr_simal}runs{nr_iterations}iters/final_maluspoints.csv')

    maluspoints = maluspoints_df['Final Maluspoints'].to_list()

    sns.histplot(maluspoints, bins=5, kde=True, edgecolor='black')
      
    # only to reproduce example case: adjust the position of the distribution  
    if nr_simal == 30 and nr_iterations == 20000:
        ax.set_xbound(0, 300)
    
    plt.xlabel('Number Maluspoints')
    plt.ylabel('Number Generated Schedules')
    plt.suptitle(f'Maluspoints Distribution Simulated Annealing', fontsize=12)
    plt.title(f'{nr_simal} runs, {nr_iterations} iterations', loc='left', fontsize=9)
    plt.savefig(f'results/simulated_annealing/final_maluspoints-{nr_simal}-{nr_iterations}.png', dpi=1200)
    plt.show()

def temperature_comparisons(schedule, nr_simal=10, nr_iterations=1000, temps: list = [50, 100, 500]):
    """
    Makes simulated annealing runs from the range min_temp to max_temp increasing 
    by step. Stores results for each temperature in separate csv.   
    """

    for temp in temps:
        
        results = []
        
        for i in range(nr_simal):
            result = []
            
            # make a simulated anneaing object 
            simulated_annealing = SimulatedAnnealing(schedule, temp)

            print(f"Running Annealing: {i}")
            
            # run algorithm number iterations amount of times  
            for j in range(nr_iterations):
                    
                    simulated_annealing.run(1)
                    
                    # append maluspoints to results of this run  
                    result.append(simulated_annealing.schedule.get_total_maluspoints())
            
            #append this run to all runs 
            results.append(result)

        values = []
        for iteration in zip(*results):
            values.append((mean(iteration), min(iteration), max(iteration)))

        with open(f"results/simulated_annealing/simulated_annealing_temp_{temp}.csv", 'w', newline='') as output_file:
            result_writer = csv.writer(output_file, delimiter=',')
            for value in values:
                result_writer.writerow(value)


def temperature_comparisons_plot(temps: list = [50, 100, 500], nr_simal=10, nr_iterations=1000):
    """
    Makes one plot comparing the results of n simulated annealing algorithms running for X
    iterations each using the same starting point but different temperatures. 
    """
    
    # collect data files 
    data_files = []

    # read in data of all temperatures 
    names = ['Avg', 'Min', 'Max']
    
    # collect names to make legend 
    temp_names = []

    for temp in temps:
        data_files.append(pd.read_csv(f'results/simulated_annealing/simulated_annealing_temp_{temp}.csv', names=names))
        temp_names.append(str(temp))
    
    fig, ax = plt.subplots()

    # plot the lines for all maluspoints 
    for i in range(len(data_files)):
        ax.plot(data_files[i]['Avg'])
    
    for i in range(len(data_files)):
        ax.fill_between(range(nr_iterations), data_files[i]['Min'], data_files[i]['Max'], alpha = 0.2)
    
    # set y axis, range 0 to 2500 works best        
    ax.set_ybound(0, 2500)
    
    ax.set_title(f'Simulated Annealing Temperatures (n={nr_simal})')
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Total Maluspoints')
    plt.legend(temp_names, title='Temperatures')

    fig.savefig(f"results/simulated_annealing/simulated_annealing_temps.png", dpi=1200)
    plt.show()