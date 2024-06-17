import random
import math

from .hillclimber import Hillclimber
from ..classes.schedule import Schedule

class SimulatedAnnealing(Hillclimber):
    # NOTE: still want to implement a way to switch between 2 types of cooling functions 
    def __init__(self, empty_schedule : Schedule, start_temperature: int, cooling_function: str = 'exponential'):
        super().__init__(empty_schedule)
        self.start_temperature = start_temperature
        self.temperature = start_temperature
        self.cooling_function = cooling_function

    def calculate_acceptance_probability(self, new_maluspoints: int, old_maluspoints: int) -> float:
        """
        Calculates the acceptance probability as a function of the old and new maluspoints,
        as well as the current temperature (self.temperature). Returning said acceptance
        probability.
        """
        delta = old_maluspoints - new_maluspoints
        
        # only do calculations if delta negative 
        if delta > 0:
            probability = 1
            
        else:
            probability = 2 ** (delta / self.temperature)

        return probability

    def update_temperature(self) -> None:
        """
        Update temperature using the specified cooling function
        """
        if self.cooling_function == 'linear':
            self.linear_temperature_decline()

        elif self.cooling_function == 'exponential':
            self.exponential_temperature_decline()

    def linear_temperature_decline(self) -> None:
        """
        Linear decline function to update temperature
        """
        self.temperature = self.start_temperature - (self.temperature / self.iterations) * self. iteration

    def exponential_temperature_decline(self):
        """
        Exponential decline function to update temperature
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
            self.reset_no_change_counter()

        else:
            self.accept_schedule(previous_schedule)
            self.revert_to_previous_schedule(previous_schedule)
            self.increase_no_change_counter()

        self.update_temperature()
