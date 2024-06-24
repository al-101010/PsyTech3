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

    def pick_roomslot(self):
        """
        Returns two random roomslots.
        """
        return random.choice(self.schedule.roomslots)
    
    def is_lecture(self, activity_type):
        """
        Return True if the activity is a lecture
        """
        return activity_type =='h'

    def pick_activity(self, activities):
        """
        Returns a random activity and it's type and course from activities.
        """
        activity = random.choice(list(activities))
        course = activity.course
        activity_type = activity.name[0]

        return activity, activity_type, course
    
    def pick_student(self, students):
        """
        Returns a random student from students.
        """
        return random.choice(list(students))
    
    def pick_students_to_switch(self, students, N):
        """
        Returns N random students from students.
        """
        random.shuffle(list(students))
        return list(students)[:N]
    
    def move_student(self, student, current_activity, switch_activity):
        """
        Moves a student from their current activity to the switch activity.
        """
        # remove current and add new activity from student's activities set
        student.activities.remove(current_activity)
        student.activities.add(switch_activity)

        student.update_schedule()

        # remove student from current and add to new activity's students set
        current_activity.students.remove(student)
        switch_activity.students.add(student)
    
    def move_student_to_new_activity(self, student, course, activity_type, new_activity):
        """
        Moves a student from their current activity to the new activity if their current 
        activity is not know.
        """
        # remove current and add new activity from student's activities set
        activities = course.activities[activity_type]
        
        for activity in activities:
            if activity != new_activity and activity in student.activities:
                self.move_student(student, activity, new_activity)

    def switch_student_from_activities(self):
        """
        Switches a student from one of their current activities to 
        another activity of the same type in the same course. 
        """
        # pick an activity to switch student from
        activity, activity_type, course = self.pick_activity(self.schedule.activities)
        
        # activity needs to be tutorial or practical, have students and have at least one other activity of same type
        while not activity.is_tutorial_practical() or len(course.activities[activity_type]) <= 1 or len(activity.students) == 0:
            activity, activity_type, course = self.pick_activity(self.schedule.activities)

        # pick student to switch
        student = self.pick_student(activity.students)
        
        # pick activity to switch student to
        switch_activity = random.choice(course.activities[activity_type])

        # pick new activity if new activity is same as first activity
        while switch_activity == activity:
            switch_activity = random.choice(course.activities[activity_type])

        # move another student to this activity if new activity is full
        if switch_activity.is_full():
            switch_student = self.pick_student(switch_activity.students)
            self.move_student(switch_student, switch_activity, activity)
        
        # move this student to other activity
        self.move_student(student, activity, switch_activity)

    def update_archive(self, activity, current_roomslot, new_roomslot):
        """ 
        When switching activities, updates the archive if activity is switched to a free room.
        """
        # split tuples in variables
        room_current, day_current, time_current = current_roomslot
        room_new, day_new, time_new = new_roomslot
        
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

    def switch_activities(self):
        """
        Switches two activities' roomslots. One activity may be empty.
        """
        # store room, day, and time of roomslot
        roomslot1 = self.pick_roomslot()
        room_1, day_1, time_1 = roomslot1

        # activities as variables
        activity_1 = room_1.schedule[day_1][time_1]
        activity_2 = self.pick_activity(self.schedule.activities)[0]

        # store roomslot of activity 2
        roomslot2 = (activity_2.room, activity_2.day, activity_2.time)
        room_2, day_2, time_2 = roomslot2

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
        self.update_archive(activity_1, roomslot1, roomslot2)
        self.update_archive(activity_2, roomslot2, roomslot1)

                       
    def create_new_activity(self, activity, activity_type, course):
        # make new activity of the same type 
        course_activities = course.activities[activity_type]
        new_name = activity_type + str(len(course_activities) + 1)
        new_activity = Activity(new_name, activity.capacity, course)

        # pick random room from still available 
        room, day, time = random.choice(self.schedule.archive)

        # schedule this new activity to an open roomslot
        new_activity.schedule(room, day, time)

        # remove room from still available 
        self.schedule.archive.remove((room, day, time)) 

        return new_activity

    def add_students_to_activity(self, new_activity, activity_type, activity_course):
        """
        Splits a work group or practical into two and reassigns students.
        Only use if free rooms available.  
        """
        # move students to new activity
        students_to_switch = self.pick_students_to_switch(activity_course.students, int(new_activity.capacity)//2)
        for student in students_to_switch:
            self.move_student_to_new_activity(student, activity_course, activity_type, new_activity)

    def add_activity_to_course(self):
        """ 
        Adds an extra activity to a course. 
        """
        # check if there are free roomslots left 
        if self.schedule.archive:

            # pick an activity to split
            activity, activity_type, course = self.pick_activity(self.schedule.activities)

            # activity can not be lecture
            while self.is_lecture(activity_type):
                activity, activity_type, course = self.pick_activity(self.schedule.activities)

            # create and schedule new activity to roomslot
            new_activity = self.create_new_activity(activity, activity_type, course)

            # add new activity to course  
            course.activities[activity_type].append(new_activity)

            # update list of total activities in schedule 
            self.schedule.activities = self.schedule.get_activities_list(self.schedule.courses)
            
            # move student to new activity
            self.add_students_to_activity(new_activity, activity_type, course)
        
    def mutate_schedule(self, number_of_mutations : int=1):
        """
        Mutate current schedule/timetable with a number of random mutations.
        """
        for mutation in range(number_of_mutations):
            if self.schedule.archive:
                mutation = random.choice([self.switch_student_from_activities, self.switch_activities, self.add_activity_to_course])
            else:
                mutation = random.choice([self.switch_student_from_activities, self.switch_activities])
            mutation()

    def display_maluspoints_division(self, title):
        """ 
        Gets all the different types of maluspoints from the schedule and prints them to terminal.
        """

        # get hold of schedule and all types of maluspoints
        print(f'Algorithm name: {title}')
        print('Maluspoints:') 
        print(f'Evening room usage: {self.schedule.room_maluspoints}')
        print(f'Free periods: {self.schedule.free_period_maluspoints}')
        print(f'Room overcapacity: {self.schedule.overcapacity_maluspoints}')
        print(f'Student double bookings: {self.schedule.double_booking_maluspoints}')
        print(f'Total: {self.schedule.total_maluspoints}')

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
        """
        Checks whether output schedule has 3 free periods (hard constraint).
        """
        for student in self.schedule.students:
            if student.three_free_periods:
                print(f"Not a valid schedule! {student} has 3 free periods.")
                return
        
        print("Valid!")