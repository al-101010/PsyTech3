from .hillclimber import Hillclimber
import copy
import random

class MutationsProbabilityClimber(Hillclimber):

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
            
            if self.iteration < 1000 or self.no_change_counter > 1000:
                switch_activities_probability = .8
            else:
                switch_activities_probability = .2

            if random.random() < switch_activities_probability:
                self.switch_activities()
            else:
                self.switch_student_from_activities()

            self.check_improvement(previous_schedule)

        # update final information in parent class
        self.maluspoints = self.schedule.get_total_maluspoints()