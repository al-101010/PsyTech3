import copy
import sys

from .random_alg import FittedStart
from .algorithm import Algorithm
from ..classes.schedule import Schedule

# increase recursion limit for deepcopies
# sadly this is a bandaid fix we were not able to fix in the timespan of this course
sys.setrecursionlimit(10**6)

class Hillclimber(Algorithm):
    """
    A class to represent a hillclimber algoirhtm.

    . . .

    Attributes
    ----------
    start_schedule: FittedStart
        starting schedule
    schedule: Schedule
        current weekly schedule
    iteration: int
        current iteration
    """
    def __init__(self, empty_schedule : Schedule, early_stopping : bool=False):
        super().__init__(empty_schedule)
        self.start_schedule = FittedStart(empty_schedule)
        self.schedule = self.start_schedule.schedule
        self.iteration = 0

    def accept_schedule(self, schedule : Schedule):
        """
        Accept given schedule by appending it's maluspoints
        """
        self.maluspoint_stats.append(schedule.get_total_maluspoints())

    def pick_number_mutations(self):
        """
        Returns the number of mutations to be done
        """
        return 1

    def check_improvement(self, previous_schedule : Schedule):
        """
        Checks whether the new schedule improves upon previous schedule (referencing maluspoints) 
        and adds the relevant maluspoints to statistics.
        If no improvement was made, resets schedule to previous state  
        """
        # compute maluspoints for previous and current schedule 
        previous_maluspoints = previous_schedule.get_total_maluspoints()
        new_maluspoints = self.schedule.get_total_maluspoints()
        # print(previous_maluspoints, new_maluspoints)

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
            
            self.iteration += 1
            
            if i % 100 == 0:
                print(i)
        
            # copy the previous schedule
            previous_schedule = copy.deepcopy(self.schedule)

            # stop if no improvements made for early stopping limit
            if self.early_stopping:

                if self.check_stagnation():
                    print("stopping early due to a stagnation of improvements")
                    return
            
            N = self.pick_number_mutations()

            # make random change to schedule and check if improved
            self.mutate_schedule(N)
            self.check_improvement(previous_schedule)

        # update final information
        self.maluspoints = self.schedule.get_total_maluspoints()

   
