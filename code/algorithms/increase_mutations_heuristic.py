from .hillclimber import Hillclimber
import copy

class IncreasingMutationsClimber(Hillclimber):

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
            if self.no_change_counter > 1800:
                mutation_count = 10
            elif self.no_change_counter > 1000:
                mutation_count = 6
            elif self.no_change_counter > 600:
                mutation_count = 4
            elif self.no_change_counter > 400:
                mutation_count = 2
            else:
                mutation_count = 1
            
            self.mutate_schedule(mutation_count)
            print(self.no_change_counter, mutation_count)

            self.check_improvement(previous_schedule)

        # update final information in parent class
        self.maluspoints = self.schedule.get_total_maluspoints()