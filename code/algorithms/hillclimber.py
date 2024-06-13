from .algorithm import Algorithm
import copy
import matplotlib.pyplot as plt
from .random_alg import Random

# importing the sys module
import sys
 
sys.setrecursionlimit(10**6)

class Hillclimber(Algorithm):
    
    def __init__(self, empty_schedule):
        super().__init__(empty_schedule)
        self.schedule = Random(empty_schedule).schedule
        self.maluspoint_stats = []
        self.early_stopping_limit = 500
        self.early_stopping_counter = 0

    def check_improvement(self, previous_schedule):
            # compute maluspoints for previous and current state 
            previous_maluspoints = previous_schedule.get_total_maluspoints()
            new_maluspoints = self.schedule.get_total_maluspoints()
            print(previous_maluspoints, new_maluspoints)

            # if improvement, reset counter and add number of maluspoint of new schedule to stats
            if new_maluspoints < previous_maluspoints:
                self.early_stopping_counter = 0
                self.maluspoint_stats.append(new_maluspoints)

            # else, increase counter and revert changes to schedule
            else:
                self.early_stopping_counter += 1
                self.schedule = previous_schedule
                self.maluspoint_stats.append(previous_maluspoints)

    def check_stagnation(self):
        return self.early_stopping_limit == self.early_stopping_counter
            

    def run(self, iters=10):
        """
        Improves the initial schedule for a number of iterations.
        Returns the final schedule when finished.
        """
        # define nr iterations or threshold
        # loop for x iterations or until threshold is reached
            # temp_schedule = switch_course()
            # temp_maluspoints = calculate maluspoints for temp schedule
            # if maluspoints are < than final_maluspoints
                # make this schedule the final schedule
                # make this schedule's maluspoints final maluspoints

        # output final schedule

        # run through all iterations
        for i in range(iters):
            # update "previous schedule"
            previous_schedule = copy.deepcopy(self.schedule)

            if i % 100 == 0:
                print(i)

            if self.check_stagnation():
                print("stopping early due to a stagnation of improvements")
                self.final_schedule = self.schedule

            # make random change to schedule
            self.mutate_schedule()

            self.check_improvement(previous_schedule)

        # update final information in parent class
        self.final_schedule = self.schedule
        self.final_maluspoints = self.schedule.get_total_maluspoints()

    def plot_graph(self, save=False):
        """
        plot maluspoints as a function of number of iterations (for hillclimber)
        ACTUALLY SEEMED GOOD TO ADD THESE TO EACH ALGORITHM SEPARATELY, AS THE PLOT 
        WILL DIFFER BETWEEN ALGORITHMS (E.G., RANDOM AND HILLCLIMBER)
        """
        iters = len(self.maluspoint_stats)
        plt.plot(self.maluspoint_stats)
        plt.xlabel('iteration')
        plt.ylabel('maluspoints')
        plt.title(f"number of iterations: {iters} & minimum maluspoints: {min(self.maluspoint_stats)}")

        if save:
            plt.savefig('../data/hillclimber_cost.png')

        plt.show()
