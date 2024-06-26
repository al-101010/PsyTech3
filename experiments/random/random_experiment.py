import matplotlib.pyplot as plt
import seaborn as sns

def run_algorithm(algorithm, schedule, iterations):
    maluspoints = []

    for i in range(iterations):
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

