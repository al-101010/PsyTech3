import random
import copy
import matplotlib.pylab as plt
from ..classes.schedule import Schedule
from ..classes.activity import Activity

class Algorithm:

    def __init__(self, schedule : Schedule, early_stopping_limit=2000):
        self.schedule = copy.deepcopy(schedule)
        self.archive = copy.copy(self.schedule.roomslots)
        self.maluspoint_stats = []
        self.early_stopping_limit = early_stopping_limit
        self.no_change_counter = 0

    def run(self):
        raise NotImplementedError

    def reset_no_change_counter(self):
        """
        Resets no change counter to 0
        """
        self.no_change_counter = 0

    def increase_no_change_counter(self):
        """
        Increases no change counter by 1
        """ 
        self.no_change_counter += 1

    def revert_to_previous_schedule(self, previous_schedule):
        """
        Reverts current schedule back to previous schedule.
        """
        self.schedule = previous_schedule

    def check_stagnation(self) -> bool:
        """
        Returns true if changes have stagnated.
        """    
        return self.early_stopping_limit == self.no_change_counter

    def update_student_schedules(self):
        """
        Update all stutdents' schedules with their current activities.
        """
        for student in self.schedule.students:
            student.update_schedule()

    def pick_roomslots_to_switch(self):
        """
        Returns two random roomslots.
        """
        # pick roomslots to switch activities from
        random_roomslot1 = random.choice(self.schedule.roomslots)
        random_roomslot2 = random.choice(self.schedule.roomslots)

        return random_roomslot1, random_roomslot2
    
    def get_roomslot_info(self, roomslot):
        """
        Returns the room, day, and time of a roomslot.
        """
        room = roomslot[0]
        day = roomslot[1]
        time = roomslot[2]

        return room, day, time

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

        # make sure activity has students
        while len(random_activity.students) == 0:
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
        
        """ Still in progress. """
        # self.update_archive(activity_1, activity_2, room_1, day_1, time_1, room_2, day_2, time_2)
    
    def update_archive(self, activity1, activity2, room1, day1, time1, room2, day2, time2):
        """ 
        When switching activities, updates the archive if activity is switched to a free room.
        
        NOTE: STILL IN PROGRESS
        """

        for item in self.archive:
            print(item)
            print((room1, day1, time1))
            print(item == (room1, day1, time1)) 

        if not activity1 and not activity2:
            # if both are free don't do anything 
            print('switched two empty rooms ')
            pass
        # check if the room slot of activity1 is free 
        elif not activity1:
            print(f'activity1 doesnt exist')
            print(f'room: {room1}, day: {day1}, time: {time1}')
            print(f'room: {room2}, day: {day2}, time: {time2}')

            # remove other activity from archive
            self.archive.remove((room1, day1, time1))
            
            # add it to archive 
            self.archive.append((room2, day2, time2))
        
        # check if the room slot of activity2 is free 
        elif not activity2: 
            print(f'activity2 doesnt exist')
            print(f'room: {room1}, day: {day1}, time: {time1}')
            print(f'room: {room2}, day: {day2}, time: {time2}')
            
            # remove other activity from archive  
            self.archive.remove((room2, day2, time2))

            # add it to archive 
            self.archive.append((room1, day1, time1))
   
        
    def switch_student_from_activities(self):
        """
        Switches a random student from one of their current activities to 
        another activity of the same type in the same course. 
        """
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

    
    def add_extra_activity(self, room, day, time):
        """
        Splits a work group or practical into two and reassigns students.
        Only use if free rooms available.  

        Question: perhaps this method and some others should be in schedule??

        TODO: 
        - change so that can also add non-random activities. 
        """

        # should work without the while loop now 
        # prevent splitting too small groups (causes errors lateron) 
        # min_len = 0 
        # need to resolve, see docstring 
        # while min_len < 20:
        #     # pick random activity from random course 
        #     random_course, type, activity = self.get_random_activity()
        #     min_len = len(activity.students)
        
        # do not get activity here if we don't want a random activity each time  
        random_course, type, activity = self.get_random_activity()

        # make new activity of the same type 
        new_name = activity.name + '.1'
        new_activity = Activity(new_name, activity.capacity, random_course)

        # schedule this new activity to an open roomslot
        new_activity.schedule(room, day, time)

        # loop over all courses in schedule 
        for course in self.schedule.courses:
            
            # find the course of the random activity to be split  
            if course.name == random_course.name:
                
                # add new activity to course activities of same type 
                course.activities[type].append(new_activity)

                # update schedule for each student in this course:
                for student in course.students:

                    # move approximately half of students to new group 
                    if activity in student.activities and len(activity.students) > len(new_activity.students):
                        self.move_student(student, activity, new_activity)

        # update activities in schedule 
        self.schedule.activities = self.schedule.get_activities_list(self.schedule.courses)

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
    
    def display_all_maluspoints(self, title):
        """ 
        Gets all the different types of maluspoints from the schedule and prints them to terminal.
        
        TODO:
        - make proper visualisation 
        """

        # get hold of schedule and all types of maluspoints
        print(f'Algorithm name: {title}')
        print('Maluspoints:') 
        print(f'Evening room usage: {self.schedule.room_maluspoints}')
        print(f'Free periods: {self.schedule.free_period_maluspoints}')
        print(f'Room overcapacity: {self.schedule.overcapacity_maluspoints}')
        print(f'Student double bookings: {self.schedule.double_booking_maluspoints}')

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
        plt.title(f'N = {iters}', loc='center', fontsize=9)
        plt.title(f'final maluspoints = {self.maluspoint_stats[-1]}', loc='left', fontsize=9)
        if save:
            plt.savefig(output_file)

        plt.show()

    def check_output_schedule(self):
        for student in self.schedule.students:
            if student.three_free_periods:
                return "Not a valid schedule! Student has 3 free periods."
        
        return "Valid!"