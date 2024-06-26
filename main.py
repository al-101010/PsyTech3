from code.algorithms.random_alg import Random, FittedStart 
from code.algorithms.hillclimber import Hillclimber
from code.algorithms.simulated_annealing import SimulatedAnnealing, ReheatSimulatedAnnealing
from code.algorithms.plant_prop import PlantProp
from code.algorithms.heuristics_hillclimber import ProblematicActivityClimber, ProblematicStudentsClimber, MutationProbabilityClimber, IncreasingMutationsClimber

from code.classes.schedule import Schedule

from experiments.hillclimber import hillclimber_experiment
from experiments.simulated_annealing import simulated_annealing_experiment
from experiments.random import random_experiment

import pandas as pd
import argparse


def main(algorithm, output_csv_name, output_png_name, experiment, iterations, early_stopping, starting_temperature, version):
    test_schedule = Schedule('data/studenten_en_vakken.csv', 'data/vakken.csv', 'data/zalen.csv')

    # ============== RANDOM ============================
    if algorithm == 'random':
        if version == 'normal':
            if not experiment: 
                # create schedule using random algorithm
                random_schedule = Random(test_schedule)

                # display malus points
                random_schedule.schedule.is_valid()
                random_schedule.display_maluspoints_division('Random')
                random_schedule.schedule.get_output(output_csv_name)

            if experiment:
                random_experiment.visualize_maluspoints_histogram(Random, test_schedule)

        if version == 'fitted':
            if not experiment:
                # create schedule using random algorithm
                fitted_schedule = FittedStart(test_schedule)

                # display malus points
                fitted_schedule.schedule.is_valid()
                fitted_schedule.display_maluspoints_division('Fitted')
                fitted_schedule.schedule.get_output(output_csv_name)
            
            if experiment:
                random_experiment.visualize_maluspoints_histogram(FittedStart, test_schedule)

    # ============== HILLCLIMBER =====================
    if algorithm == 'hillclimber':
        if version == 'normal':
            if not experiment:
                hillclimber = Hillclimber(test_schedule, early_stopping)
                hillclimber.run(iterations)
                hillclimber.schedule.is_valid()
                hillclimber.display_maluspoints_division('Hillclimber')

                hillclimber.plot_graph(output_png_name, title='Hillclimber Algorithm', save=True)
                hillclimber.schedule.get_output(output_csv_name)

            if experiment:
                hillclimber_experiment.get_averages(test_schedule, 'hillclimber')
                hillclimber_experiment.plot_averages('hillclimber')
                hillclimber_experiment.plot_maluspoints_distribution('hillclimber')
                hillclimber_experiment.plot_zoom('hillclimber')
                

        if version == 'problematic activity':
            if not experiment:
                problematic_activity_climber = ProblematicActivityClimber(test_schedule, early_stopping)
                problematic_activity_climber.run(iterations)
                problematic_activity_climber.schedule.is_valid()
                problematic_activity_climber.display_maluspoints_division('Problematic Activity Climber')

                problematic_activity_climber.plot_graph(output_png_name, title='Problematic Activity Climber', save=True)
                problematic_activity_climber.schedule.get_output(output_csv_name)
            
            if experiment:
                hillclimber_experiment.get_averages(test_schedule, 'problematic_activity')
                hillclimber_experiment.plot_averages('problematic_activity')
                hillclimber_experiment.plot_maluspoints_distribution('problematic_activity')
                hillclimber_experiment.plot_zoom('problematic_activity')
                

        if version == 'problematic students':
            if not experiment:
                problematic_student_climber = ProblematicStudentsClimber(test_schedule, early_stopping)
                problematic_student_climber.run(iterations)
                problematic_student_climber.schedule.is_valid()
                problematic_student_climber.display_maluspoints_division('Problematic Student Climber')

                problematic_student_climber.plot_graph(output_png_name, title='Problematic Student Climber', save=True)
                problematic_student_climber.schedule.get_output(output_csv_name)

            if experiment:
                hillclimber_experiment.get_averages(test_schedule, 'problematic_students')
                hillclimber_experiment.plot_averages('problematic_students')
                hillclimber_experiment.plot_maluspoints_distribution('problematic_students')
                hillclimber_experiment.plot_zoom('problematic_students')
                

        if version == 'mutation probability':
            if not experiment:
                mutation_probability_climber = MutationProbabilityClimber(test_schedule, early_stopping)
                mutation_probability_climber.run(iterations)
                mutation_probability_climber.schedule.is_valid()
                mutation_probability_climber.display_maluspoints_division('Mutation Probability Climber')

                mutation_probability_climber.plot_graph(output_png_name, title='Mutation Probability Climber', save=True)
                mutation_probability_climber.schedule.get_output(output_csv_name)

            if experiment:
                hillclimber_experiment.get_averages(test_schedule, 'mutation_probability')
                hillclimber_experiment.plot_averages('mutation_probability')
                hillclimber_experiment.plot_maluspoints_distribution('mutation_probability')
                hillclimber_experiment.plot_zoom('mutation_probability')


        if version == 'increasing mutations':
            if not experiment:
                increasing_mutations_climber = IncreasingMutationsClimber(test_schedule, early_stopping)
                increasing_mutations_climber.run(iterations)
                increasing_mutations_climber.schedule.is_valid()
                increasing_mutations_climber.display_maluspoints_division('Increasing Mutations Climber')

                increasing_mutations_climber.plot_graph(output_png_name, title='Increasing Mutation Climber', save=True)
                increasing_mutations_climber.schedule.get_output(output_csv_name)
            
            if experiment:
                hillclimber_experiment.get_averages(test_schedule, 'increasing_mutations')
                hillclimber_experiment.plot_averages('increasing_mutations')
                hillclimber_experiment.plot_maluspoints_distribution('increasing_mutations')
                hillclimber_experiment.plot_zoom('increasing_mutations')

    # ======== PLANT PROPAGATION ===============
    if algorithm == 'plantprop':
        plantprop = PlantProp(test_schedule, early_stopping=early_stopping)
        plantprop.run(iterations)
        plantprop.schedule.is_valid()
        plantprop.display_maluspoints_division('Plantprop')

        plantprop.plot_graph(output_png_name, title='PlantProp Algorithm', save=True)
        plantprop.schedule.get_output(output_csv_name)

    # ========= SIMULATED ANNEALING ============
    if algorithm == 'simulated annealing':
        if version == 'normal':
            if not experiment:
                #create annealing schedule
                simulated_annealing = SimulatedAnnealing(test_schedule, starting_temperature, cooling_function='exponential', early_stopping=early_stopping)
                simulated_annealing.run(iterations)
                simulated_annealing.schedule.is_valid()
                simulated_annealing.display_maluspoints_division('Simulated Annealing')

                simulated_annealing.plot_graph(output_png_name, title='Simulated Annealing Algorithm', save=True)
                simulated_annealing.schedule.get_output(output_csv_name)
            
            if experiment:
                # simulated annealing experiment
                simulated_annealing_experiment.get_averages(test_schedule)
                simulated_annealing_experiment.plot_averages()
                simulated_annealing_experiment.plot_maluspoints_distribution()
                simulated_annealing_experiment.plot_zoom()

                # temperature experiment
                simulated_annealing_experiment.temperature_comparisons(test_schedule)
                simulated_annealing_experiment.temperature_comparisons_plot()
        
        # ========= REHEATED SIMULATED ANNEALING ===============
        if version == 'reheated':
            # create schedule
            reheat_simulated_annealing = ReheatSimulatedAnnealing(test_schedule, starting_temperature, cooling_function='exponential', reheat_threshold=1200, early_stopping=early_stopping)
            reheat_simulated_annealing.run(iterations)
            reheat_simulated_annealing.schedule.is_valid()
            reheat_simulated_annealing.display_maluspoints_division('Reheat Simulated Annealing')

            reheat_simulated_annealing.plot_graph(output_png_name, title='Reheat Simulated Annealing Algorithm', save=True)
            reheat_simulated_annealing.schedule.get_output(output_csv_name)

    
if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "run algorithm to create timetable")

    # Adding arguments
    parser.add_argument("algorithm", help = "algorithm to run")
    parser.add_argument("output_csv", help = "output file (csv)")
    parser.add_argument("output_png", help = "output plot (png)")
    parser.add_argument("-e", "--experiment", action="store_true", help = "experiment (default: False)")
    parser.add_argument("-i", "--iterations", type=int, default = 50000, help="iterations (default: 1930)")
    parser.add_argument("-es", "--early_stopping", action="store_true", help="early stopping(default: False)")
    parser.add_argument("-st", "--starting_temperature",   type=int, default = 50, help="starting temperature (default: 50)")
    parser.add_argument("-v", "--version", type=str, default='normal', help="algorithm version (default: normal)")

    # Read arguments from command line
    args = parser.parse_args()
    
    # Run main with provide arguments
    main(args.algorithm, args.output_csv, args.output_png, args.experiment, args.iterations, args.early_stopping, args.starting_temperature, args.version)