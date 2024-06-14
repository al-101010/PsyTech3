import random
import copy
import matplotlib.pylab as plt
from ..classes.schedule import Schedule

class Algorithm:

    def __init__(self, schedule : Schedule, early_stopping_limit=1000):
        self.schedule = copy.deepcopy(schedule)
        self.archive = copy.copy(self.schedule.roomslots)
        self.maluspoint_stats = []
        self.early_stopping_limit = early_stopping_limit
        self.no_improvement_counter = 0

    def run(self):
        raise NotImplementedError

    def reset_no_improvement_counter(self):
        """
        Resets no improvement counter to 0
        """
        self.no_improvement_counter = 0

    def increase_no_improvement_counter(self):
        """
        Increases no improvement counter by 1
        """ 
        self.no_improvement_counter += 1

    def revert_to_previous_schedule(self, previous_schedule):
        """
        Reverts current schedule back to previous schedule.
        """
        self.schedule = previous_schedule

    def check_stagnation(self) -> bool:
        """
        Returns true if improvements have stagnated.
        """    
        return self.early_stopping_limit == self.no_improvement_counter

    def update_student_schedules(self):
        """
        Update all stutdents' schedules with their current activities.
        """
        for student in self.schedule.students:
            student.update_schedule()

    def pick_roomslots_to_switch(self):
        # pick roomslots to switch activities from
        random_roomslot1 = random.choice(self.schedule.roomslots)
        random_roomslot2 = random.choice(self.schedule.roomslots)

        return random_roomslot1, random_roomslot2
    
    def get_roomslot_info(self, roomslot):
        room = roomslot[0]
        day = roomslot[1]
        time = roomslot[2]

        return room, day, time

    def switch_activities(self):
        """
        Switches the activities from two randomly chosen roomslots. Activity may
        also be None.
        """
        # store room, day, and time of roomslots
        random_roomslot1, random_roomslot2 = self.pick_roomslots_to_switch()
        room_1, day_1, time_1 = self.get_roomslot_info(random_roomslot1)
        room_2, day_2, time_2 = self.get_roomslot_info(random_roomslot2)

        # save activities in roomslots
        activity_1 = room_1.schedule[day_1][time_1]
        activity_2 = room_2.schedule[day_2][time_2]

        # if activity is Activity instance, schedule instance
        if activity_1:
            activity_1.schedule(room_2, day_2, time_2)
        if activity_2:
            activity_2.schedule(room_1, day_1, time_1)
        
        # switch the activities to the other roomslot in room instance
        room_1.schedule[day_1][time_1] = activity_2
        room_2.schedule[day_2][time_2] = activity_1

        self.update_student_schedules()

    def get_random_activity(self):
        """
        Returns the course, activity type, and activity instance of a 
        randomly chosen tutorial or practical that has at least one
        other activity of that same type.
        """
         # pick a random course
        random_course = random.choice(self.schedule.courses)
        
        # make sure the course has tutorials or practicals
        while not ('w' or 'p') in random_course.activities:
            random_course = random.choice(self.schedule.courses)

        # choose random activity type
        random_activity_type = random.choice(list(random_course.activities))

        # make sure activity type has more than 1 activities and is not a lecture
        while len(random_course.activities[random_activity_type]) <= 1 or random_activity_type == 'h':
            random_activity_type = random.choice(list(random_course.activities))

        # pick a random tutorial or practical
        random_activity = random.choice(random_course.activities[random_activity_type])

        return random_course, random_activity_type, random_activity
    
    def move_student(self, student, current_activity, switch_activity):
        """
        Moves a student from their curren activity to the switch activity.
        """
        # remove current and add new activity from student's activities set
        student.activities.remove(current_activity)
        student.activities.add(switch_activity)

        student.update_schedule()

        # remove student from current and add to new activity's students set
        current_activity.students.remove(student)
        switch_activity.students.add(student)

    def switch_student_from_activities(self):
        ##TODO: I still need to implement switching two students if an activity is full

        random_course, random_activity_type, random_activity = self.get_random_activity()

        # pick a random students from the tutorial/practical
        random_student = random.choice(list(random_activity.students))

        # pick another random activity to switch student to
        switch_activity = random.choice(random_course.activities[random_activity_type])

        # pick new activity if new activity is same as random activity
        while switch_activity == random_activity:
            switch_activity = random.choice(random_course.activities[random_activity_type])

        # move the student to the new activity if activity is not full
        if not len(switch_activity.students) == switch_activity.capacity:
            self.move_student(random_student, random_activity, switch_activity)

        # if the other tutorial is full pick another or switch students?


    def mutate_schedule(self, number_of_mutations : int=1):
        """
        Mutate current schedule/timetable with a number of random mutations.
        INCOMPLETE -> need to add more ways to alter the schedule
        = Useful when we have multiple ways of altering the schedule (as we don't want to make every
        single alteration at ones)
        """

        for i in range(number_of_mutations):
            mutation = random.choice([self.switch_student_from_activities, self.switch_activities])

            mutation()
    
    def plot_graph(self, output_file : str, x : str='iteration', y : str='maluspoints', title : str='Algorithm', save: bool=False):
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
        plt.title(f"number of iterations = {iters} & minimum maluspoints = {min(self.maluspoint_stats)}")

        if save:
            plt.savefig(output_file)

        plt.show()