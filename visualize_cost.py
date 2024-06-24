import matplotlib.pyplot as plt
import seaborn as sns

from code.classes.schedule import Schedule
from code.algorithms.random_alg import Random
from code.algorithms.fitted_start import FittedStart

def run_algorithm(algorithm, schedule, iterations):
    maluspoints = []

    for i in range(iterations):
        print(i)
        random_schedule = algorithm(schedule)
        maluspoints.append(random_schedule.schedule.get_total_maluspoints())

    return maluspoints

def visualize_maluspoints_barplot(algorithm, schedule, iterations, output_file):
    maluspoints = run_algorithm(algorithm, schedule, iterations)
    sns.histplot(maluspoints, bins=50, kde=True, edgecolor='black')
    plt.xlabel('Number Maluspoints')
    plt.ylabel('Number Generated Schedules')
    plt.title('Distribution of maluspoints over generated schedules')
    plt.savefig(output_file)


schedule = Schedule('data/studenten_en_vakken.csv', 'data/vakken.csv', 'data/zalen.csv')
# visualize_maluspoints_barplot(Random, schedule, 10000, '../data/random_cost.png')

visualize_maluspoints_barplot(FittedStart, schedule, 10000, 'data/fitted_start.png')