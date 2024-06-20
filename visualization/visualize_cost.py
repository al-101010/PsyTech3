import matplotlib.pyplot as plt
import seaborn as sns

from code.classes.schedule import Schedule
from code.algorithms.random_alg import Random

def run_algorithm(algorithm, schedule, iterations):
    maluspoints = []

    for i in range(iterations):
        print(i)
        random_schedule = algorithm(schedule)
        maluspoints.append(random_schedule.schedule.get_total_maluspoints())

    return maluspoints

def visualize_maluspoints_barplot(algorithm, schedule, iterations):
    maluspoints = run_algorithm(algorithm, schedule, iterations)
    sns.histplot(maluspoints, bins=50, kde=True, edgecolor='black')
    plt.xlabel('Number Maluspoints')
    plt.ylabel('Number Generated Schedules')
    plt.title('Distribution of maluspoints over randomly generated schedules')
    plt.savefig('../data/random_cost.png')


schedule = Schedule('data/studenten_en_vakken.csv', 'data/vakken.csv', 'data/zalen.csv')
visualize_maluspoints_barplot(Random, schedule, 10000)
