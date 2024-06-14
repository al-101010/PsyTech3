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


    def check_improvement(self, previous_schedule):
        """
        Checks whether the new schedule improves upon previous schedule (referencing maluspoints) 
        and adds the relevant maluspoints to statistics.
        If no improvement was made, resets schedule to previous state  
        """
        # compute maluspoints for previous and current state 
        previous_maluspoints = previous_schedule.get_total_maluspoints()
        new_maluspoints = self.schedule.get_total_maluspoints()
        print(previous_maluspoints, new_maluspoints)

        # if improvement, reset counter and add number of maluspoint of new schedule to stats
        if new_maluspoints < previous_maluspoints:
            self.no_improvement_counter = 0
            self.maluspoint_stats.append(new_maluspoints)
        elif new_maluspoints == previous_maluspoints:
            self.no_improvement_counter += 1
            self.maluspoint_stats.append(new_maluspoints)
        # else, increase counter and revert changes to schedule
        else:
            self.no_improvement_counter += 1
            self.schedule = previous_schedule
            self.maluspoint_stats.append(previous_maluspoints)
        
        print(self.no_improvement_counter)

    def check_stagnation(self) -> bool:
        """
        Checks whether improvements have stagnated
        """    
        return self.early_stopping_limit == self.no_improvement_counter
            

    def run(self, iters=10):
        """
        Improves the initial schedule for a number of iterations.
        Returns the final schedule when finished.
        """
        # run through all iterations
        for i in range(iters):

            # update "previous schedule"
            previous_schedule = copy.deepcopy(self.schedule)

            if i % 100 == 0:
                print(i)

            # stop if no general improvements made
            if self.check_stagnation():
                print("stopping early due to a stagnation of improvements")
                self.final_schedule = self.schedule
                return

            # make random change to schedule
            self.mutate_schedule()

            self.check_improvement(previous_schedule)

        # update final information in parent class
        self.maluspoints = self.schedule.get_total_maluspoints()

    def plot_graph(self, save: bool =False):
        """
        Plot maluspoints as a function of number of iterations (for hillclimber)
        """
        # intialize variables
        iters = len(self.maluspoint_stats)

        # plot graph
        plt.plot(self.maluspoint_stats)
        plt.xlabel('iteration')
        plt.ylabel('maluspoints')
        plt.suptitle(f"Hillclimber Algorithm", fontsize=12)
        plt.title(f"number of iterations = {iters} & minimum maluspoints = {min(self.maluspoint_stats)}")

        if save:
            plt.savefig('data/hillclimber_cost.png')

        plt.show()
