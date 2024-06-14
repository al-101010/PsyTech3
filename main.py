from code.algorithms.sequential import Sequential # Ignore : True
from code.algorithms.random_alg import Random
from code.algorithms.hillclimber import Hillclimber
from code.algorithms.simulated_annealing import SimulatedAnnealing
from code.classes.schedule import Schedule
import pandas as pd
import time

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

    # # create schedule using random algorithm
    # random_schedule = Random(test_schedule)

    # # # calculate malus points
    # maluspoints = random_schedule.schedule.get_total_maluspoints()
    # print(f"This schedule resulted in {maluspoints} maluspoints.")
    # # print(f"Evening room usage: {random_schedule.schedule.get_evening_room_maluspoints()}")

    # print(get_output(random_schedule.schedule.students, 'data/random_output.csv'))

    # create hillclimber schedule
    start_time = time.time()

    simulated_annealing = SimulatedAnnealing(test_schedule, 500)
    simulated_annealing.run(2000)

    print("--- %s seconds ---" % (time.time() - start_time))

    simulated_annealing.plot_graph('data/simulated_annealing_plot.png', title='Simulated Annealing Algorithm', save=False)
    print(get_output(simulated_annealing.schedule.students, 'data/simulated_annealing.csv'))
    # print(simulated_annealing.maluspoints)


    

