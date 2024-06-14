import random
import math

from .hillclimber import Hillclimber
from ..classes.schedule import Schedule

class SimulatedAnnealing(Hillclimber):
    # NOTE: still want to implement a way to switch between 2 types of cooling functions 
    def __init__(self, empty_schedule : Schedule, start_temperature: int):
        super().__init__(empty_schedule)
        self.start_temperature = start_temperature
        self.temperature = start_temperature

    def calculate_acceptance_probability(self, new_maluspoints: int, old_maluspoints: int) -> float:
        """
        Calculates the acceptance probability as a function of the old and new maluspoints,
        as well as the current temperature (self.temperature). Returning said acceptance
        probability.
        """
        delta = new_maluspoints - old_maluspoints
        try:
            probability = math.exp(-delta / self.temperature)
        
        except OverflowError:
            probability = float('inf')
            
        return probability

    def update_temperature(self) -> None:
        """
        Update temperature using the specified cooling function
        """
        self.temperature = self.start_temperature * (0.99 ** self.iteration)

    def check_improvement(self, previous_schedule: Schedule) -> None:
        """
        Checks and accepts schedules better than the current/previous one, and sometimes
        accepts worse schedules, depending on the acceptance probability
        """
        # compute maluspoints
        previous_maluspoints = previous_schedule.get_total_maluspoints()
        new_maluspoints = self.schedule.get_total_maluspoints()

        # obtain acceptance probability
        probability = self.calculate_acceptance_probability(new_maluspoints, previous_maluspoints)

        # if random number between 0 and 1 lower than probability accept change
        if random.random() < probability:
            self.accept_schedule(self.schedule)

        else:
            self.accept_schedule(previous_schedule)
            self.revert_to_previous_schedule(previous_schedule)

        self.update_temperature()
