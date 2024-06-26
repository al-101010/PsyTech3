# PsyTech3

## Case : Lectures & Lesroosters

### Problem specification: 
For study period 4 at Science Park, students have enrolled in courses. Each course can have 
several of the following study formats each week: lectures, tutorials, practicals.
Each of these study formats needs to be scheduled in one of seven lecture rooms, which 
have a certain capacity of students to sit. The task is to make a schedule for the lecture rooms 
and students to fit all study activities for each course as effectively as possible.

## Installation
### Requirements
This codebase was programmed using python 3.10.13, the requirements.txt file contains all the need packages to run the code succesfully.
Download this code base by running the following line in your terminal:

```git clone https://github.com/al-101010/PsyTech3.git```

Install all required packages by running the following line in your terminal:

```pip install -r requirements.txt```

### Usage
The algorithms created to solve our problem can be run by calling:

```python main.py algorithm output_csv output_png [-e] [-i] [-st] [-v]```

Below the different parse arguments and their possible values are explained:
1. algorithm - the algorithm you want to run.
    - 'random'
    - 'hillclimber'
    - 'simulated annealing'
    - 'plantprop'
2. output_csv - the location where you want to store the final schedule of the algorithm as a csv file on your computer.
3. output_png - the location where you want to store the graph of maluspoints over time of the algorithm.
4. [-e] - Boolean that denotes whether you want to run experiments with this algorithm.
    - Default is False
5. [-i] - the number of iterations you want the algorithm to run for.
    - Default is 50000
6. [-st] - the starting temperature for simulated annealing.
    - Default is 50
7. [-v] - the version of the algorithm you want to run.
    - 'normal' runs the regular version of any algorithm, this is also the default.
    - 'reheated' runs reheated simulated annealing if algorithm is 'simulated annealing'
    - 'problematic activity' runs a hillclimber with the heuristic of choosing activities with the most maluspoints when swapping.
    - 'problematic students' runs a hillclimber with the heuristic of choosing students with most maluspoints when switching.
8. [-es] - Boolean that denotes whether you want to run the algorithm with early stopping enabled.
    - Default is False

### Structure
This list describes the most important folders and files and where to find them:
- **/code**: contains all the code of this project
    - **/code/algorithms**: contains all code for the algorithms
    - **/code/classes**: contains all code for the classes of our data structure
    - **/code/visualization**: contains the code for visualizing a created schedule.
- **/data**: contains the data files of all students, courses, and rooms that have to be used in the schedule
- **/experiments**: contains all the experiments we ran for each algorithm.
- **/results**: contains all the results for the experiments we ran for each algorithm.

## Experiments 
There are 7 experiment files included in this repository, each testing one specific algorithm. 
This includes running the respective algorithm n times for a specified number of iterations and collecting:  

- a) the average, minimum, and maximum maluspoints per iteration over all runs 
- b) the final maluspoints after each run  
- c) the final output schedules of n runs 

After the data has been collected into the respective csv files, the time to conduct the experiment is printed to the screen (in seconds). 

Data a) is plotted to showcase the reduction in cost (maluspoints) over iterations and per algorithm. Note that the plot displays not only the total maluspoints but also their constituents (e.g. double booking of students). 
Data b) is plotted into a histogram of the distribution of final maluspoints per run. 

### Running an experiment 
To run an experiment, set the argparse arguments in the following way 
- **algorithm** to the algorithm of choice
- **output_csv** to output.csv (not needed for experiments)
- **output_png** to output.png (not needed for experiments)
- **-i** to any number (not needed for experiments)
- **-st** to any number (if using simulated annealing, not needed for experiments)
- **-e** add to run experiment
- **-v** to the version of choice

Attention: By default, an experiment runs the respective algorithm for 20000 iterations 30 times! This can take up to 17 hours or more with a slow machine. It is possible to test different values by specifying this in the functions in main.py. Below is an example of how to do that: 

To run a hillclimber experiment 10 times with 10 iterations specify in main: 
- *hillclimber_experiment.hillclimb_all_averages(test_schedule, 10, 10)*
- *hillclimber_experiment.ratios_plot(10, 10)*
- *hillclimber_experiment.plot_maluspoints_distribution(10, 10)*

Running this, you should find a new folder in results with your experiment data and plots. 

Note that for these types of experiments you can comment out the *ratios_plot_zoom()* function as this is mainly a way to zoom in to a specific area of a plot for a better insight into the different maluspoints.  

## Visualizations
### Visualize.py
A schedule consists of the following components:
1. Students
2. Courses
3. Rooms

Each of these components has it's own schedule that can be visualized. This can be done in *visualize.py* by calling the following:

```
python visualize.py schedule_type name [-s]
```

1. schedule_type - denotes which component you want a schedule from.
    - 'student'
    - 'course'
    - 'room'
2. name - denotes the name or id of the component you want a schedule from.
    - e.g 'Yanick Abbing' as student
    - e.g 'Heuristieken 2' as course
    - e.g 'C0.110' as room
3. -s - denotes the file path that holds your csv file
    - default is set to '../../results/hillclimber/tested_hillclimber_output_500K.csv' since this path holds our schedule with the least maluspoints found.

### ICS visualization
To be able to interact with the complete schedule we also created a script that reads a schedule output file as an ICS file for each course. 

This file can be run by simply calling:

```
python ics_visualization.py
```

Running this file will write an ICS file to the course_schedules folder for each course. Opening each ICS file and adding it to your calendar will show you the created schedule for the week of june 24 - june 28. 

It is recommended to save each file as a different calendar with a different color so it is more clear which course is which. Searching for a student name in the search bar will also show that student's personal schedule.

## Authors: 
- Daimy van Loo 
- Daantje de Laaf
- Alexandra Genis


