from code.algorithms import simulated_annealing as sa
from code.algorithms import random_alg as rd

import matplotlib.pyplot as plt
import random 
import csv
from statistics import mean


def simal_averages(schedule, nr_simal=10, nr_iterations=1000, temp=500):
    
    # add a seed for randomness 
    random.seed(123)

    # initialise results 
    results = []
    
    # define how many algorithms you want to run 
    for i in range(nr_simal):
        
        # store results of each algorithm run 
        result = []
        
        # make an algorithm object  
        algorithm = sa.SimulatedAnnealing(schedule, temp)
        
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


def simal_averages_plot(nr_simal=10, file_name="results/simulated_annealing/simulated_annealing_averages.csv"):
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
    ax.set_title(f'Simulated Annealing Algorithms (n={nr_simal})')
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Average Maluspoints')
    ax.set_ybound(0, 4000)
    fig.savefig("results/simulated_annealing/simulated_annealing_averages.png")


def simal_temp_comparisons(schedule, n_simal=10, n_iters=1000, min_temp=200, max_temp=1100, step=100):
    """
    Makes simulated annealing runs from the range min_temp to max_temp increasing 
    by step. Stores results for each temperature in separate csv.   
    """

    # add seed
    random.seed(123)

    for n in range(min_temp, max_temp, step):
        results = []
        for i in range(n_simal):
            result = []
            
            # make a simulated anneaing object 
            simulated_annealing = sa.SimulatedAnnealing(schedule, n)
            
            print(f"Running Annealing: {i}")
            # run algorithm n_iters amount of times  
            for j in range(n_iters):
                    simulated_annealing.run(1)
                    # append maluspoints to results of this run  
                    result.append(simulated_annealing.schedule.get_total_maluspoints())
            #append this run to all runs 
            results.append(result)

        values = []
        for iteration in zip(*results):
            values.append((mean(iteration), min(iteration), max(iteration)))

        with open(f"results/simulated_annealing/simulated_annealing_temp_{n}.csv", 'w', newline='') as output_file:
            result_writer = csv.writer(output_file, delimiter=',')
            for value in values:
                result_writer.writerow(value)

def simal_temp_comparisons_plot(min_temp=500, max_temp=1100, step=100, n_simal=10):
    """
    Makes one plot comparing the results of n simulated annealing algorithms running for X
    iterations each using the same starting point but different temperatures. 
    """
    fig, ax = plt.subplots()
    results = []
    for n in range(min_temp, max_temp, step):
        with open(f"results/simulated_annealing/simulated_annealing_temp_{n}.csv", 'r') as input_file:
            result_reader = csv.reader(input_file, delimiter=',')
            results.append([float(value) for value, _, _ in result_reader])

    for temp, result in zip(range(min_temp, max_temp, step), results):
        ax.plot(result, label=f'Temperature {temp}')

    ax.legend(loc='upper right')
    ax.set_title(f'Simulated Annealing Temperatures (n={n_simal})')
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Total Maluspoints')
    fig.savefig(f"results/simulated_annealing/simulated_annealing_temp.png")





