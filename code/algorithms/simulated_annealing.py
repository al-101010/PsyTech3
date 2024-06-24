import random
import copy
import math
import matplotlib.pyplot as plt

from .hillclimber import Hillclimber
from ..classes.schedule import Schedule
from .heuristics_hillclimber import HeuristicsHillclimber

class SimulatedAnnealing(Hillclimber):
    
    def __init__(self, empty_schedule : Schedule, start_temperature: int, cooling_function: str = 'boltzexp'):
        super().__init__(empty_schedule)
        self.start_temperature = start_temperature
        self.temperature = start_temperature
        self.cooling_function = cooling_function
        self.switched_cooling_functions = False
        self.best_schedule = empty_schedule
        self.best_maluspoints = float('inf')

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

        elif self.cooling_function == 'boltz':
            self.boltz_temperature_decline()

        elif self.cooling_function == 'boltzexp':
            self.boltz_exp_temperature_decline()

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
    
    def boltz_temperature_decline(self):
        self.temperature = self.start_temperature / math.log(self.iteration + 1)

    def boltz_exp_temperature_decline(self):
        if self.iteration <= (self.iterations // 5) and not self.switched_cooling_functions:
            self.boltz_temperature_decline()

        elif not self.switched_cooling_functions:
            self.iteration = 1
            self.start_temperature = self.temperature
            self.switched_cooling_functions = True
            self.exponential_temperature_decline()

        else:
            self.exponential_temperature_decline()

    def check_improvement(self, previous_schedule: Schedule) -> None:
        """
        Checks and accepts schedules better than the current/previous one, and sometimes
        accepts worse schedules, depending on the acceptance probability
        """
        # compute maluspoints
        previous_maluspoints = previous_schedule.get_total_maluspoints()
        new_maluspoints = self.schedule.get_total_maluspoints()
        print(previous_maluspoints, new_maluspoints)

        # obtain acceptance probability
        probability = self.calculate_acceptance_probability(new_maluspoints, previous_maluspoints)

        # if random number between 0 and 1 lower than probability accept change
        if random.random() < probability:
            self.accept_schedule(self.schedule)
            if new_maluspoints < self.best_maluspoints and new_maluspoints < 200:
                self.best_schedule = copy.deepcopy(self.schedule)
                self.best_maluspoints = new_maluspoints

            if new_maluspoints < previous_maluspoints:
                self.reset_no_change_counter()

            else:
                self.increase_no_change_counter()

        else:
            self.accept_schedule(previous_schedule)
            self.revert_to_previous_schedule(previous_schedule)
            self.increase_no_change_counter()

        self.update_temperature()

    def plot_graph(self, output_file : str, x : str='iteration', y : str='maluspoints', title: str='Simulated Annealing Algorithm', save: bool=False):
        """
        Plots statistics and also reports the starting temperature
        """
        
        main_title = f"Simulated Annealing Algoritm"
        
        plt.title(f'start temperature = {self.start_temperature}', loc='right', fontsize=9)

        super().plot_graph(output_file, x, y, main_title, save)

    def run(self, iters):
        """
        Improves the initial schedule for a number of iterations.
        Returns the best schedule when finished.
        """
        super().run(iters)
        self.schedule = self.best_schedule
        self.maluspoints = self.best_maluspoints


class ReheatSimulatedAnnealing(SimulatedAnnealing):
    def __init__(self, empty_schedule : Schedule, start_temperature: int, cooling_function: str = 'exponential', reheat_temperature: int = 10, reheat_threshold: int = 1500):
        super().__init__(empty_schedule, start_temperature, cooling_function)
        self.reheat_temperature = reheat_temperature
        self.reheat_threshold = reheat_threshold
    
    
    def reheat(self):
        print("reheating... :)")
        self.temperature = self.reheat_temperature

    def check_improvement(self, previous_schedule: Schedule) -> None:
        super().check_improvement(previous_schedule)

        # if self.no_change_counter >= self.reheat_threshold:
        if self.no_change_counter >= self.reheat_threshold and self.temperature <= 1:
            self.reheat()
            self.reset_no_change_counter()
            self.iteration = 0

    def plot_graph(self, output_file : str, x : str='iteration', y : str='maluspoints', title: str='Reheat Simulated Annealing Algorithm', save: bool=False):
        """
        Plot maluspoints as a function of number of iterations (for hillclimber)
        """
        # intialize variables
        iters = len(self.maluspoint_stats)

        # plot graph
        plt.plot(self.maluspoint_stats)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.suptitle(title, fontsize=12)
        plt.title(f'N = {iters}', loc='center', fontsize=9)
        plt.title(f'minimum maluspoints = {min(self.maluspoint_stats)}', loc='left', fontsize=9)
        plt.title(f'start temperature = {self.start_temperature}', loc='right', fontsize=9)

        if save:
            plt.savefig(output_file)

        plt.show()
