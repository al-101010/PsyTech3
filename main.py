from code.algorithms.random_alg import Random
from code.algorithms.hillclimber import Hillclimber
from code.algorithms.simulated_annealing import SimulatedAnnealing, ReheatSimulatedAnnealing
from code.algorithms.plant_prop import PlantProp
from code.algorithms.heuristics_hillclimber import ProblematicActivityClimber, ProblematicStudentsClimber, MutationProbabilityClimber, IncreaseMutationsClimber

from experiments.hillclimber import hillclimber_experiment
from experiments.simulated_annealing import simulated_annealing_experiment
from experiments.reheating import reheating_experiment

from code.classes.schedule import Schedule
import pandas as pd
import time
import argparse

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


def main(algorithm, output_csv_name, output_png_name, experiment, iterations, starting_temperature, version):
    test_schedule = Schedule('data/studenten_en_vakken.csv', 'data/vakken.csv', 'data/zalen.csv')

    if algorithm == 'random':
        # create schedule using random algorithm
        random_schedule = Random(test_schedule)

        # display malus points
        random_schedule.display_maluspoint_division('Random')
        get_output(random_schedule.schedule.students, output_csv_name)


    if algorithm == 'hillclimber':
    
        hillclimber_schedule = Hillclimber(test_schedule)
        hillclimber_schedule.run(iterations)
        hillclimber_schedule.display_maluspoints_division('Hillclimber')

        hillclimber_schedule.plot_graph(output_png_name, title='Hillclimber Algorithm', save=True)
        get_output(hillclimber_schedule.schedule.students, output_csv_name)

        if experiment:
            hillclimber_experiment.hillclimb_all_averages(test_schedule)
            hillclimber_experiment.hillclimber_ratios_plot()
            hillclimber_experiment.hillclimber_ratios_plot_zoom()
            hillclimber_experiment.read_in_schedules()
            hillclimber_experiment.timed_hillclimber_runs(test_schedule, Hillclimber) 
            
            # comparison of two hillclimbers 
            # hillclimber_experiment.hillclimb(test_schedule, algorithm=Hillclimber, name='Hillclimber')
            # hillclimber_experiment.hillclimb(test_schedule, algorithm=TargetedHillclimber, name='TargetedClimber')
            # hillclimber_experiment.compare_hillclimbers("results/hillclimber/Hillclimber30_iter1000.csv", "results/hillclimber/TargetedClimber_30_iter1000.csv")


    if algorithm == 'plantprop':
        plantprop = PlantProp(test_schedule)
        plantprop.run(iterations)
        plantprop.display_maluspoints_division('Plantprop')

        plantprop.plot_graph(output_png_name, title='PlantProp Algorithm', save=True)
        get_output(plantprop.schedule.students, output_csv_name)


    if algorithm == 'simulated annealing':
        if version == 'normal':
            #create annealing schedule
            simulated_annealing = SimulatedAnnealing(test_schedule, starting_temperature, cooling_function='exponential')
            simulated_annealing.run(iterations)
            simulated_annealing.display_all_maluspoints('Simulated Annealing')

            simulated_annealing.plot_graph(output_png_name, title='Simulated Annealing Algorithm', save=False)
            get_output(simulated_annealing.schedule.students, output_csv_name)
            
            if experiment:
                simulated_annealing_experiment.simal_all_averages(test_schedule)
                simulated_annealing_experiment.simal_all_averages_plot()
                simulated_annealing_experiment.simal_temp_comparisons(test_schedule)
                simulated_annealing_experiment.simal_temp_comparisons_plot()

        if version == 'reheated':
            # create schedule
            reheat_simulated_annealing = ReheatSimulatedAnnealing(test_schedule, starting_temperature, cooling_function='exponential', reheat_threshold=1200)
            reheat_simulated_annealing.run(iterations)
            reheat_simulated_annealing.display_all_maluspoints('Reheat Simulated Annealing')

            reheat_simulated_annealing.plot_graph(output_png_name, title='Reheat Simulated Annealing Algorithm', save=True)
            get_output(reheat_simulated_annealing.schedule.students, output_csv_name)
            print(reheat_simulated_annealing.maluspoints)
            
            if experiment:
                reheating_experiment.reheating_averages(test_schedule)
                reheating_experiment.reheating_plot()

    
if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "run algorithm to create timetable")

    # Adding arguments
    parser.add_argument("algorithm", help = "algorithm to run")
    parser.add_argument("output_csv", help = "output file (csv)")
    parser.add_argument("output_png", help = "output plot (png)")
    parser.add_argument("-e", "--experiment", type=bool, default = False, help = "experiment (default: False)")
    parser.add_argument("-i", "--iterations", type=int, default = 20000, help="iterations (default: 1930)")
    parser.add_argument("-t", "--starting_temperature",   type=int, default = 50, help="starting temperature (default: 50)")
    parser.add_argument("-v", "--version", type=str, default='normal', help="algorithm version (default: normal)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.algorithm, args.output_csv, args.output_png, args.experiment, args.iterations, args.starting_temperature, args.version)