from ..classes.schedule import Schedule
from .add_activities import Algorithm
from .hillclimber import Hillclimber
import copy
import random
import math
import matplotlib.pyplot as plt


class PlantProp(Algorithm):
    
    def __init__(self, schedule: Schedule, children_parameter : int=5000, mutation_parameter : float=.01, N : int=5, early_stopping_limit=1000):
        super().__init__(schedule, early_stopping_limit)
        self.N = N
        self.population = []
        self.children_parameter = children_parameter
        self.mutation_parameter = mutation_parameter
        self.evaluation_stats = []
        self.iteration = 0

        self.create_start_population()

    def get_population_maluspoints(self):
        population_maluspoints = []
        for hillclimber in self.population:
            population_maluspoints.append(hillclimber.schedule.get_total_maluspoints())
        
        return population_maluspoints

    def create_start_population(self):
        for n in range(self.N):
            self.population.append(Hillclimber(self.schedule))
    
    def update_population(self):
        self.population = sorted(self.population, key= lambda x: x.schedule.get_total_maluspoints())[:self.N]

    def get_best_schedule(self):
        best_hillclimber = sorted(self.population, key= lambda x: x.schedule.get_total_maluspoints())[0]
        return best_hillclimber.schedule
    
    def get_worst_schedule(self):
        worst_hillclimber = sorted(self.population, key= lambda x: x.schedule.get_total_maluspoints(), reverse=True)[0]
        return worst_hillclimber.schedule
    
    def check_improvement(self, previous_maluspoints, current_maluspoints):
        return current_maluspoints < previous_maluspoints
    
    def get_fitness(self, hillclimber):
        hillclimber_maluspoints = hillclimber.schedule.get_total_maluspoints()
        best_maluspoints = self.get_best_schedule().get_total_maluspoints()
        worst_maluspoints = self.get_worst_schedule().get_total_maluspoints()
        return .5*(math.tanh(4 * ((best_maluspoints - hillclimber_maluspoints) / (best_maluspoints - worst_maluspoints)) - 2) + 1)
    
    def calculate_children(self, hillclimber, n_max=10):
        fitness = self.get_fitness(hillclimber)
        random_number = random.random()
        return math.ceil(fitness*random_number*n_max)
    
    def calculate_mutations(self, hillclimber, m_max=20):
        fitness = self.get_fitness(hillclimber)
        random_number = random.random()
        return math.ceil((1-fitness)*random_number*m_max)
    
    def mutate_all(self):
        children = []
        for hillclimber in self.population:
            for child in range(self.calculate_children(hillclimber)):
                hillclimber = copy.deepcopy(hillclimber)
                hillclimber.mutate_schedule(self.calculate_mutations(hillclimber))
                children.append(hillclimber)
        
        self.population += children

    def run(self, iters=10):
        while self.iteration < iters:
            previous_best_maluspoints = self.get_best_schedule().get_total_maluspoints()
            self.mutate_all()
            self.iteration += len(self.population)
            self.update_population()
            current_best_maluspoints = self.get_best_schedule().get_total_maluspoints()
            self.evaluation_stats.append(self.iteration)
            self.maluspoint_stats.append(current_best_maluspoints)

            if self.check_improvement(previous_best_maluspoints, current_best_maluspoints):
                self.no_change_counter = 0
            else:
                self.no_change_counter += 1

            if self.check_stagnation():
                self.maluspoints = current_best_maluspoints
                self.schedule = self.get_best_schedule()
                print("stopping early due to a stagnation of improvements")
                return

            print(self.iteration, self.get_best_schedule().get_total_maluspoints())

        self.schedule = self.get_best_schedule()
        self.maluspoints = self.schedule.get_total_maluspoints()

    def plot_graph(self, output_file : str, x : str='iteration', y : str='maluspoints', title : str='Algorithm', save: bool=False):
        """
        Plot maluspoints as a function of number of iterations (for hillclimber)
        """

        # plot graph
        plt.plot(self.evaluation_stats, self.maluspoint_stats)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.suptitle(title, fontsize=12)
        plt.title(f'N = {self.iteration}', loc='center', fontsize=9)
        plt.title(f'final maluspoints = {self.maluspoint_stats[-1]}', loc='left', fontsize=9)
        if save:
            plt.savefig(output_file)

        plt.show()
            
    
