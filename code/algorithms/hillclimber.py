import copy
import sys
from .random_alg import Random
from .algorithm import Algorithm
from ..classes.schedule import Schedule

# increase recursion limit for deepcopies
sys.setrecursionlimit(10**6)

class Hillclimber(Algorithm):
    
    def __init__(self, empty_schedule : Schedule):
        super().__init__(empty_schedule)
        self.random_start = Random(empty_schedule)
        self.schedule = self.random_start.schedule
        self.archive = self.random_start.archive
        self.iteration = 0

    def accept_schedule(self, schedule : Schedule):
        """
        Accept given schedule by appending it's maluspoints
        """
        self.maluspoint_stats.append(schedule.get_total_maluspoints())

    def check_improvement(self, previous_schedule : Schedule):
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
            self.reset_no_change_counter()
            self.accept_schedule(self.schedule)
        elif new_maluspoints == previous_maluspoints:
            self.increase_no_change_counter()
            self.accept_schedule(self.schedule)
        # else, increase counter and revert changes to schedule
        else:
            self.increase_no_change_counter()
            self.revert_to_previous_schedule(previous_schedule)
            self.accept_schedule(previous_schedule)
        
    def run(self, iters  : int=10):
        """
        Improves the initial schedule for a number of iterations.
        Returns the final schedule when finished.
        """
        self.iterations = iters
        
        # run through all iterations
        for i in range(1, iters + 1):
            
            self.iteration = i
            
            if i % 100 == 0:
                print(i)

            # update "previous schedule"
            previous_schedule = copy.deepcopy(self.schedule)

            # stop if no general improvements made
            if self.check_stagnation():
                print("stopping early due to a stagnation of improvements")
                return

            # make random change to schedule
            self.mutate_schedule()

            self.check_improvement(previous_schedule)

        # update final information in parent class
        self.maluspoints = self.schedule.get_total_maluspoints()

   
