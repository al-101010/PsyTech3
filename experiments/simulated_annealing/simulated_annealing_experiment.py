from code.algorithms import simulated_annealing as sa
from code.algorithms import random_alg as rd

import matplotlib.pyplot as plt
import random 
import csv
from statistics import mean

"""
TODOs:
- fix same axis for plot
- add temperature
"""


def simal_averages(schedule, nr_algorithms, nr_iterations):
    
    # add a seed for randomness 
    random.seed(123)

    # initialise results 
    results = []
    
    # define how many algorithms you want to run 
    for i in range(nr_algorithms):
        
        # store results of each algorithm run 
        result = []
        
        # make an algorithm object  
        algorithm = sa.SimulatedAnnealing(schedule, 500)
        
        print(f"Running Simulated Annealing Algorithm Number: {i}")
        # run the algorithm X times 
        for j in range(nr_iterations):
            
            # run the algorithm for one iteration 
            algorithm.run(1)

            # append maluspoints for this iteration to results   
            result.append(algorithm.schedule.get_total_maluspoints())

        # append result to all results 
        results.append(result)

    # get all values for a row 
    values = []
    for iteration in zip(*results):
        values.append((mean(iteration), min(iteration), max(iteration)))

    with open("results/simulated_annealing/simulated_annealing_averages.csv", 'w', newline='') as output_file:
        result_writer = csv.writer(output_file, delimiter=',')
        
        for value in values:
            result_writer.writerow(value)


def simal_averages_plot(nr_algorithms, file_name="results/simulated_annealing/simulated_annealing_averages.csv"):
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

    ax.plot(averages, label='Simulated Annealing')
    ax.fill_between(range(0, len(averages)), minima, maxima, alpha=0.5, linewidth=0)
    ax.set_title(f'Simulated Annealing Algorithms (n={nr_algorithms}, iters/run={len(results)})')
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Average Maluspoints')
    ax.set_ybound(0, 3000)
    fig.savefig("results/simulated_annealing/simulated_annealing_averages.png")


def simulated_annealing_temperature_comparisons_plot():
    fig, ax = plt.subplots()
    results = []
    for n in range(1, 60, 10):
        with open(f"results/simulatedannealing/simulatedannealing_temp_{n}.csv", 'r') as input_file:
            result_reader = csv.reader(input_file, delimiter=',')
            results.append([float(value) for value, _, _ in result_reader])

    for temp, result in zip(range(1, 60, 10), results):
        ax.plot(result, label=f'Temperature {temp}')

    ax.legend(loc='upper right')
    ax.set_title('Sim Annealing Temperatures (n=...)')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Total Maluspoints')
    fig.savefig(f"results/simulatedannealing/simulatedannealing_temp_{n}.png")





