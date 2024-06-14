from ..classes.schedule import Schedule
from .algorithm import Algorithm
from .hillclimber import Hillclimber
import copy


class PlantProp(Algorithm):
    
    def __init__(self, schedule: Schedule, children_parameter : int=1000, mutation_parameter : float=.01, N : int=5, early_stopping_limit=1000):
        super().__init__(schedule, early_stopping_limit)
        self.N = N
        self.population = []
        self.children_parameter = children_parameter
        self.mutation_parameter = mutation_parameter

        self.create_start_population()

    def get_population_maluspoints(self):
        population_maluspoints = []
        for hillclimber in self.population:
            population_maluspoints.append(hillclimber.schedule.get_total_maluspoints())
        
        return population_maluspoints

    
    def create_start_population(self):
        for n in range(self.N):
            self.population.append(Hillclimber(self.schedule))

    def calculate_children(self, schedule):
        return max(int(self.children_parameter / schedule.get_total_maluspoints()), 1)
    
    def calculate_mutations(self, schedule):
        return max(int(self.mutation_parameter * schedule.get_total_maluspoints()), 1)
    
    def mutate_all(self):
        population = copy.deepcopy(self.population)
        children = []
        for hillclimber in population:
            schedule = hillclimber.schedule
            for child in range(self.calculate_children(schedule)):
                hillclimber.mutate_schedule(self.calculate_mutations(schedule))
                children.append(hillclimber)
        
        self.population += children

    def update_population(self):
        self.population = sorted(self.population, key= lambda x: x.schedule.get_total_maluspoints())[:self.N]

    def get_best_schedule(self):
        best_hillclimber = sorted(self.population, key= lambda x: x.schedule.get_total_maluspoints())[0]
        return best_hillclimber.schedule

    def run(self, iters=10):
        for i in range(iters):
            self.mutate_all()
            self.update_population()
            self.maluspoint_stats.append(self.get_best_schedule().get_total_maluspoints())

            print(i, self.get_best_schedule().get_total_maluspoints())

        self.final_schedule = self.get_best_schedule()
        self.maluspoints = self.final_schedule.get_total_maluspoints()
            
    