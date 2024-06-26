import matplotlib.pyplot as plt
import seaborn as sns

def run_algorithm(algorithm, schedule, runs):
    """
    Runs random start algorithm for a number of run
    and keeps track of maluspoints of each run.
    """
    maluspoints = []

    # loop for runs
    for i in range(runs):

        # fill the random schedule and append it's maluspoints
        random_schedule = algorithm(schedule)
        maluspoints.append(random_schedule.schedule.get_total_maluspoints())

    return maluspoints

def visualize_maluspoints_histogram(algorithm, schedule, runs=1000):
    """
    Visualizes the distribution of maluspoints at the end of each run.
    """
    maluspoints = run_algorithm(algorithm, schedule, runs)

    # plot histogram
    sns.histplot(maluspoints, bins=50, kde=True, edgecolor='black')
    plt.xlabel('Number Maluspoints')
    plt.ylabel('Number Generated Schedules')
    plt.title('Distribution of maluspoints over randomly generated schedules')
    plt.savefig(f'results/random/{algorithm}_cost.png')

