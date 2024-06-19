import random
import copy
import matplotlib.pylab as plt
from ..classes.schedule import Schedule
from ..classes.activity import Activity

class Algorithm:

    def __init__(self, schedule : Schedule, early_stopping_limit=2000):
        self.schedule = copy.deepcopy(schedule)
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
        
        # update the archive if an activity is switched to an empty spot 
        self.update_archive(activity_1, room_1, day_1, time_1, room_2, day_2, time_2)
        self.update_archive(activity_2, room_2, day_2, time_2, room_1, day_1, time_1)
    
    def update_archive(self, activity, room_current, day_current, time_current, room_new, day_new, time_new):
        """ 
        When switching activities, updates the archive if activity is switched to a free room.
        """
    
        # if there is no activity in a room slot  
        if not activity:
            # loop over still available rooms 
            for item in self.schedule.archive:
                # if room, day, time are found in archive 
                if room_current.room_number == item[0].room_number and day_current == item[1] and time_current == item[2]:
                    # remove old activity from archive 
                    self.schedule.archive.remove(item)
                    # add new activity to archive 
                    self.schedule.archive.append((room_new, day_new, time_new)) 
                    break
   
        
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

        # move another student to this activity if new activity is full
        if len(switch_activity.students) == switch_activity.capacity:
            switch_student = random.choice(list(switch_activity.students))
            self.move_student(switch_student, switch_activity, random_activity)
        
        # move this student to other activity
        self.move_student(random_student, random_activity, switch_activity)
        

        # if the other tutorial is full pick another or switch students?

    def split_activity(self):
        """ 
        Splits an activity into two and assigns the new activity to a still free roomslot. 

        TODO: don't use get_random_activity() but get an activity from the list of 
        activities with many maluspoints. 
        """
        if len(self.schedule.archive) > 0:
            print('splitting activity')

            random_course, activity_type, activity = self.get_random_activity()

            # pick random room from still available 
            room, day, time = random.choice(self.schedule.archive)
            
            # add an activity of same type  
            self.add_extra_activity(random_course, activity_type, activity, room, day, time)
            
            # remove room from still available 
            self.schedule.archive.remove((room, day, time))


    def add_extra_activity(self, activity_course, activity_type, activity, room, day, time):
        """
        Splits a work group or practical into two and reassigns students.
        Only use if free rooms available.  

        Question: perhaps this method and some others should be in schedule??

        TODO: 
        - NOTE: if added to mutations gets very slow. probable cause: use of deepcopy. 
        waiting for representation update. before proceeding.  

        """
        
        # make new activity of the same type 
        new_name = activity.name[0] + str(int(activity.name[1]) + len(activity_course.activities[activity_type]))
        new_activity = Activity(new_name, activity.capacity, activity_course)
        

        # schedule this new activity to an open roomslot
        new_activity.schedule(room, day, time)

        # add new activity to course  
        activity_course.activities[activity_type].append(new_activity)

        # update student courses 
        for student in activity_course.students: 
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
            
            if self.no_change_counter < 1000:
                mutation = random.choice([self.switch_student_from_activities, self.switch_activities])
            else:
                mutation = random.choice([self.switch_student_from_activities, self.switch_activities, self.split_activity])

            # testing ##################
            #mutation = self.split_activity
            #print('Split activity')
            # mutation = self.switch_activities
            # for student in self.schedule.students:
            #     print(f' student maluspoints {student.maluspoints}')

            # if self.no_change_counter > 1000:
        
            #     mutation = random.choice([self.switch_student_from_activities, self.switch_activities, self.split_activity])
            #     if mutation == self.split_activity:
            #         print('Split activity')
            ############################
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
                print(f"Not a valid schedule! {student} has 3 free periods.")
                return
        
        print("Valid!")