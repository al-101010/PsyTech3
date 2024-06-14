import random

from .hillclimber import Hillclimber
from ..classes.schedule import Schedule

class SimulatedAnnealing(Hillclimber):
    
    def __init__(self, empty_schedule : Schedule, start_temperature):
        super().__init__(empty_schedule)
        self.start_temperature = start_temperature
        self.temperature = start_temperature

    def calculate_acceptance_probability(self, new_maluspoints, old_maluspoints):
        return

    def update_temperature(self, iteration):
        self.temperature = self.start_temperature * (0.99 ** iteration)

    def check_improvement(self, previous_schedule):
        
        # compute maluspoints
        previous_maluspoints = previous_schedule.get_total_maluspoints()
        new_maluspoints = self.schedule.get_total_maluspoints()

        # obtain acceptance probability
        probability = self.calculate_acceptance_probability()

        # if random number between 0 and 1 lower than probability accept change
        if random.random() < probability:
            self.accept_schedule(self.schedule)

        else:
            self.accept_schedule(previous_schedule)
            self.revert_to_previous_schedule(previous_schedule)

        self.update_temperature()
