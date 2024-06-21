from code.algorithms import simulated_annealing as sa

import matplotlib.pyplot as plt
import random 
import csv
from statistics import mean

def reheating_averages(schedule, nr_algorithms=10, nr_iterations=1000, temp=500):
    
    # add a seed for randomness 
    random.seed(123)

    # initialise results 
    results = []
    
    # define how many algorithms you want to run 
    for i in range(nr_algorithms):
        
        # store results of each algorithm run 
        result = []
        
        # make an algorithm object  
        algorithm = sa.ReheatSimulatedAnnealing(schedule, temp)
        
        print(f"Running Reheated Simulated Annealing Algorithm Number: {i}")
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

    with open("results/reheating/reheating_averages.csv", 'w', newline='') as output_file:
        result_writer = csv.writer(output_file, delimiter=',')
        
        for value in values:
            result_writer.writerow(value)

def reheating_averages_plot(nr_algorithms=10, file_name="results/reheating/reheating_averages.csv"):
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

    ax.plot(averages, label='Reheated Simulated Annealing')
    ax.fill_between(range(0, len(averages)), minima, maxima, alpha=0.5, linewidth=0)
    ax.set_title(f'Reheated Simulated Annealing Algorithms (n={nr_algorithms})')
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Average Maluspoints')
    ax.set_ybound(0, 4000)
    fig.savefig("results/reheating/reheating_averages.png")