from algorithm import Algorithm
import copy
import matplotlib.pyplot as plt
from random_alg import Random

class Hillclimber(Algorithm):
    
    def __init__(self, empty_schedule):
        super.__init__(empty_schedule)
        self.schedule = Random(empty_schedule)
        self.maluspoint_stats = []

    def improve_schedule(self, iters=10):
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

        previous_schedule = copy.deepcopy(self.schedule)
        early_stopping_limit = 1000
        early_stopping_counter = 0

        # run through all iterations
        for i in range(iters):

            # check whether stagnates
            if early_stopping_limit == early_stopping_counter:
                print("stopping early due to a stagnation of improvements")
                self.final_schedule = self.schedule
                return
            
            # make random change to schedule
            self.mutate_schedule()

            # compute maluspoints for previous and current state 
            previous_maluspoints = previous_schedule.get_total_maluspoints()
            new_maluspoints = self.schedule.get_total_maluspoints()

            # if improvement, reset counter and add number of maluspoint of new schedule to stats
            if new_maluspoints <= previous_maluspoints:
                early_stopping_counter = 0
                self.statistics.append(new_maluspoints)

            # else, increase counter and revert changes to schedule
            else:
                early_stopping_counter += 1
                self.schedule = previous_schedule
                self.statistics.append(previous_maluspoints)

            # update "previous schedule"
            previous_schedule = copy.deepcopy(self.schedule)
        
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
        plt.plot(range(1, iters + 1), self.maluspoint_stats)
        plt.xlabel('iteration')
        plt.ylabel('maluspoints')
        plt.title(f"number of iterations: {iters} & minimum maluspoints: {min(self.maluspoint_stats)}")

        if save:
            plt.savefig('../data/hillclimber_cost.png')

        plt.show()
