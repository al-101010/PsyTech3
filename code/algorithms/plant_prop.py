import copy
import random
import math
import matplotlib.pyplot as plt

from ..classes.schedule import Schedule
from .algorithm import Algorithm
from .hillclimber import Hillclimber



class PlantProp(Algorithm):
    """
    A class to represent a schedule.

    . . .

    Attributes
    ----------
    N: int
        size of population at start of each iteration
    population: list[Hillclimber]
        a list of all current hillclimbers
    evaluation_stats: list[int]
        a list of the total number of evaluations after each iteration
    evaluation: int
        running counter of number of evaluations
    """
    def __init__(self, schedule: Schedule, N : int=10):
        super().__init__(schedule)
        self.N = N
        self.population = []
        self.evaluation_stats = []
        self.evaluation = 0

        self.create_start_population()

    def get_population_maluspoints(self) -> list:
        """
        Return a list of maluspoints for each schedule in the population
        """
        population_maluspoints = []

        # loop over each hillclimber in population and append it's schedule's maluspoints
        for hillclimber in self.population:
            population_maluspoints.append(hillclimber.schedule.get_total_maluspoints())
        
        return population_maluspoints

    def create_start_population(self) -> None:
        """
        Adds N hillclimbers to start population.
        """
        for n in range(self.N):
            self.population.append(Hillclimber(self.schedule))
    
    def update_population(self) -> None:
        """
        Update population to be the best N hillclimbers.
        """
        self.population = sorted(self.population, key= lambda x: x.schedule.get_total_maluspoints())[:self.N]

    def get_best_or_worst_schedule(self, worst : bool) -> Schedule:
        """
        Return the schedule of the best hillclimber in population.
        """
        hillclimber = sorted(self.population, key= lambda x: x.schedule.get_total_maluspoints(), reverse=worst)[0]
        return hillclimber.schedule
    
    def check_improvement(self, previous_maluspoints : int, current_maluspoints : int) -> bool:
        """
        Check if maluspoints of current schedule have improved from previous schedule.
        """
        return current_maluspoints < previous_maluspoints
    
    def get_fitness(self, hillclimber : Hillclimber) -> float:
        """
        Return the fitness of a hillclimber.
        """
        # get this climber's maluspoints
        hillclimber_maluspoints = hillclimber.schedule.get_total_maluspoints()

        # get best and worst maluspoints from population
        best_maluspoints = self.get_best_or_worst_schedule(worst=False).get_total_maluspoints()
        worst_maluspoints = self.get_best_or_worst_schedule(worst=True).get_total_maluspoints()

        # calculate fitness
        fitness = .5*(math.tanh(4 * ((best_maluspoints - hillclimber_maluspoints) / (best_maluspoints - worst_maluspoints + .1)) - 2) + 1)
        
        return fitness
    
    def calculate_children(self, hillclimber : Hillclimber, n_max : int=10) -> int:
        """
        Return the number of children this hillclimber should make,
        maximum amount of children default is 10.
        """
        # get fitness and random number to calculate children
        fitness = self.get_fitness(hillclimber)
        random_number = random.random()

        return math.ceil(fitness*random_number*n_max)
    
    def calculate_mutations(self, hillclimber : Hillclimber, m_max=20):
        """
        Return the number of mutations this hillclimber should make,
        maximum amount of mutations default is 20.
        """
        # get fitness and random number to calculate mutations
        fitness = self.get_fitness(hillclimber)
        random_number = random.random()

        return math.ceil((1-fitness)*random_number*m_max)
    
    def mutate_all(self) -> None:
        """
        Mutate all schedules with their calculated amount of children 
        and mutations.
        """
        children = []

        # loop over all hill climbers and their number of children
        for hillclimber in self.population:
            for child in range(self.calculate_children(hillclimber)):

                # mutate the child and append it to the list of children
                hillclimber = copy.deepcopy(hillclimber)
                hillclimber.mutate_schedule(self.calculate_mutations(hillclimber))
                children.append(hillclimber)
        
        # add children to population
        self.population += children

    def run(self, evals : int=10) -> None:
        """
        Run plant propagation for a number of evaluations.
        """
        # loop while current evaluation is lower than specified evaluataions
        while self.evaluation < evals:
            
            previous_best_maluspoints = self.get_best_schedule().get_total_maluspoints()
            
            self.mutate_all()
            
            self.evaluation += len(self.population)
            
            self.update_population()
            
            current_best_maluspoints = self.get_best_schedule().get_total_maluspoints()
            
            # append evaluations and best maluspoint status to plot later
            self.evaluation_stats.append(self.evaluation)
            self.maluspoint_stats.append(current_best_maluspoints)

            # update no change counter according to imrpovement
            if self.check_improvement(previous_best_maluspoints, current_best_maluspoints):
                self.no_change_counter = 0
            else:
                self.no_change_counter += 1

            # implement early stopping if stagnation
            if self.early_stopping:
                if self.check_stagnation():

                    # save best schedule and maluspoints
                    self.maluspoints = current_best_maluspoints
                    self.schedule = self.get_best_schedule()

                    print("stopping early due to a stagnation of improvements")
                    return

        # save best schedule and maluspoints
        self.schedule = self.get_best_schedule()
        self.maluspoints = self.schedule.get_total_maluspoints()

    def plot_graph(self, output_file : str, x : str='evaluation', y : str='maluspoints', title : str='Algorithm', save: bool=False):
        """
        Plot maluspoints as a function of number of evaluations (for hillclimber)
        """

        # plot graph
        plt.plot(self.evaluation_stats, self.maluspoint_stats)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.suptitle(title, fontsize=12)
        plt.title(f'N = {self.evaluation}', loc='center', fontsize=9)
        plt.title(f'final maluspoints = {self.maluspoint_stats[-1]}', loc='left', fontsize=9)
        if save:
            plt.savefig(output_file)

        plt.show()
            
    
