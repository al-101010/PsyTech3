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
    - 'problematic students' runs a hillclimber with the heuristic of choosing students with mose maluspoints when switching.

### structure
This list describes the most important folders and files and where to find them:
- **/code**: contains all the code of this project
    - **/code/algorithms**: contains all code for the algorithms
    - **/code/classes**: contains all code for the classes of our data structure
    - **/code/visualization**: contains the code for visualizing a schedule
- **/data**: contains the data files of all students, courses, and rooms that have to be used in the schedule
    
## Authors: 
- Daimy van Loo 
- Daantje de Laaf
- Alexandra Genis

## Dankwoord (Acknowledgments):



