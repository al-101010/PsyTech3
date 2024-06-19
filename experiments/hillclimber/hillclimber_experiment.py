from code.algorithms import hillclimber as hc
from code.algorithms import random_alg as rd

import matplotlib.pyplot as plt
import random 
import csv
from statistics import mean

"""
TODOs:
- fix same axis for plot
- finalise plot different types of maluspoints 
"""


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
        climber = hc.Hillclimber(schedule)
        
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

    ax.plot(averages, label='HillClimber')
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





