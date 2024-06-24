from code.algorithms.sequential import Sequential # Ignore : True
from code.algorithms.random_alg import Random
from code.algorithms.hillclimber import Hillclimber
from code.algorithms.simulated_annealing import SimulatedAnnealing, ReheatSimulatedAnnealing
from code.algorithms.plant_prop import PlantProp
from code.algorithms.targeted_hillclimber import TargetedHillclimber
from code.algorithms.mutation_probability_heuristic import MutationsProbabilityClimber
from code.algorithms.heuristics_hillclimber import HeuristicsHillclimber

from experiments.hillclimber import hillclimber_experiment
from experiments.simulated_annealing import simulated_annealing_experiment
from experiments.reheating import reheating_experiment

from code.classes.schedule import Schedule
import pandas as pd
import time

start_time = time.time()
print("--- %s seconds ---" % (time.time() - start_time))

def get_output(students : list, output : str):
        """
        Print output schedule as data frame and convert to csv.
        """
        rows = []

        # loop over all activities of each student and append relevant info
        for student in students:
            for activity in student.activities:
                rows.append([student.name, activity.course, activity.name, activity.room.room_number, activity.day, activity.time])

        # create dataframe of schedule
        schedule = pd.DataFrame(rows, columns=['Student', 'Vak', 'Activiteit', 'Zaal', 'Dag', 'Tijdslot'])

        schedule.to_csv(output, index=False)

        return schedule


if __name__ == "__main__":
    test_schedule = Schedule('data/studenten_en_vakken.csv', 'data/vakken.csv', 'data/zalen.csv')

    # --------------------- RANDOM -----------------------------------------
    # # create schedule using random algorithm
    # random_schedule = Random(test_schedule)

    # # calculate malus points
    # maluspoints = random_schedule.schedule.get_total_maluspoints()
    # print(f"This schedule resulted in {maluspoints} maluspoints.")
    # print(f"Evening room usage: {random_schedule.schedule.get_evening_room_maluspoints()}")
    # get_output(random_schedule.schedule.students, 'data/random_output.csv')


    # # # --------------------- HILLCLIMBER -------------------------------------
    # hillclimber_schedule = Hillclimber(test_schedule)
    # hillclimber_schedule.run(100)
    # hillclimber_schedule.display_all_maluspoints('Hillclimber')

    # hillclimber_schedule.plot_graph('data/tested_hillclimber_cost.png', title='Hillclimber Algorithm', save=False)
    # get_output(hillclimber_schedule.schedule.students, 'data/tested_hillclimber_output.csv')

    # hillclimber_experiment.hillclimb_all_averages(test_schedule)
    # hillclimber_experiment.hillclimber_ratios_plot()
    # hillclimber_experiment.hillclimber_ratios_plot_zoom()
    # hillclimber_experiment.read_in_schedules()
    # hillclimber_experiment.timed_hillclimber_runs(test_schedule, Hillclimber) # not sure if keeping
    
    # comparison of two hillclimbers 
    # hillclimber_experiment.hillclimb(test_schedule, algorithm=Hillclimber, name='Hillclimber')
    # hillclimber_experiment.hillclimb(test_schedule, algorithm=TargetedHillclimber, name='TargetedClimber')
    # hillclimber_experiment.compare_hillclimbers("results/hillclimber/Hillclimber30_iter1000.csv", "results/hillclimber/TargetedClimber_30_iter1000.csv")


    # --------------------- PLANT PROPAGATION ----------------------------------
    # plantprop = PlantProp(test_schedule)
    # plantprop.run(100)
    # plantprop.display_all_maluspoints('Plantprop')

    # plantprop.plot_graph('data/plantprop_cost.png', title='PlantProp Algorithm', save=True)
    # get_output(plantprop.schedule.students, 'data/plantprop_output.csv')


    # # --------------------- SIMULATED ANNEALING --------------------------------
    # create annealing schedule
    # simulated_annealing = SimulatedAnnealing(test_schedule, 50, cooling_function='exponential')
    # simulated_annealing.run(50000)
    # simulated_annealing.display_all_maluspoints('Simulated Annealing')

    # simulated_annealing.plot_graph('data/simulated_annealing_plot.png', title='Simulated Annealing Algorithm', save=False)
    # print(get_output(simulated_annealing.schedule.students, 'data/boltzexp_simulated_annealing.csv'))
    
    
    # print(simulated_annealing.maluspoints)

    # simulated_annealing_experiment.simal_averages(test_schedule)
    # simulated_annealing_experiment.simal_averages_plot()
    # simulated_annealing_experiment.simal_temp_comparisons(test_schedule)
    # simulated_annealing_experiment.simal_temp_comparisons_plot()
    
    # # # --------------------- REHEATED SIMULATED ANNEALING --------------------------------
    # create schedule
    # reheat_simulated_annealing = ReheatSimulatedAnnealing(test_schedule, 50, cooling_function='exponential', reheat_threshold=1200)
    # reheat_simulated_annealing.run(50000)
    # reheat_simulated_annealing.display_all_maluspoints('Reheat Simulated Annealing')

    # reheat_simulated_annealing.plot_graph('data/boltzexp_reheat_simulated_annealing_plot.png', title='Reheat Simulated Annealing Algorithm', save=True)
    # print(get_output(reheat_simulated_annealing.schedule.students, 'data/boltzexp_reheat_simulated_annealing.csv'))
    # print(reheat_simulated_annealing.maluspoints)

    #reheating_experiment.reheating_averages(test_schedule)
    #reheating_experiment.reheating_plot()



    # --------------------- HEURISTIC - BUSY FIRST HILLCLIMBER --------------------------------
    # # create busy first schedule 
    # busy_climber = BusyClimber(test_schedule)
    # busy_climber.run(100)
    # busy_climber.display_all_maluspoints('Busy First Hillclimber')
    
    # # get results 
    # busy_climber.plot_graph('data/busy_climber_plot.png', title='Busy Comes First Heuristic', save=False)
    # print(get_output(busy_climber.schedule.students, 'data/busy_climber.csv'))
    # print(busy_climber.maluspoints)


    # --------------------- HEURISTIC - EXHAUSTIVE HILLCLIMBER --------------------------------
    # # create exhaustive schedule 
    # exhaustive_climber = ExhaustiveClimber(test_schedule)
    # exhaustive_climber.run(100)
    # exhaustive_climber.display_all_maluspoints('Exhaustive Hillclimber')
    
    # # get results 
    # exhaustive_climber.plot_graph('data/exhaustive_climber_plot.png', title='Exhaustive Schedule Heuristic', save=True)
    # print(get_output(exhaustive_climber.schedule.students, 'data/exhaustive_climber.csv'))
    # print(exhaustive_climber.maluspoints)

    # --------------------- HEURISTIC - TARGETED HILLCLIMBER --------------------------------
    # # create targeted schedule 
    # targeted_climber = TargetedHillclimber(test_schedule)
    # targeted_climber.run(20000)
    # targeted_climber.display_all_maluspoints('Targeted Hillclimber')
    
    # # # get results 
    # targeted_climber.plot_graph('data/targeted_climber_plot.png', title='Targeted Schedule Heuristic', save=True)
    # print(get_output(targeted_climber.schedule.students, 'data/targeted_climber.csv'))

    # --------------------- HEURISTIC - MUTATION PROBABILITY HILLCLIMBER --------------------------------
    # # create targeted schedule 
    # mutation_probability_climber = MutationsProbabilityClimber(test_schedule)
    # mutation_probability_climber.run(20000)
    # mutation_probability_climber.display_all_maluspoints('mutation_probability Hillclimber')
    # mutation_probability_climber.check_output_schedule()
    
    # # get results 
    # mutation_probability_climber.plot_graph('data/mutation_probability_climber_plot.png', title='mutation_probability Schedule Heuristic', save=False)
    # print(get_output(mutation_probability_climber.schedule.students, 'data/mutation_probability_climber.csv'))
