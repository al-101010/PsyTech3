

class Student:

    def __init__(self, name : str, number : str, course_names = set[str]) -> None:
        self.name = name
        self.student_number = number
        self.course_names = course_names
        self.courses = set()
        self.activities = set()
        self.schedule = self.empty_schedule()
        self.maluspoints = 0

    def __repr__(self) -> str:
        return self.name


    def add_courses(self, all_courses : set):
        """
        Add a student's courses to the set of courses as course class instances.
        Also removes NA values.
        """
        for course in all_courses:
            if course.name in self.course_names:
                self.courses.add(course)


    def empty_schedule(self, days : list[str] = ['ma', 'di', 'wo', 'do', 'vr'], timeslots : list[str] = ['9', '11', '13', '15', '17']):
        """
        Returns an empty schedule for this student, all timeslots are labeled 'free'.
        """

        schedule = {}

        # loop over each day and create a key
        for day in days:
            schedule[day] = {}

            # loop over each time slot and label it 'free'
            for timeslot in timeslots:
                schedule[day][timeslot] = 'Free'

        return schedule


    def personal_schedule(self):
        """
        Add student's activities to their schedule and return this schedule.
        """
        # loop over all activities of this student and add it to relevant day and time in schedule.
        for activity in self.activities:
            
            # initialize list for timeslot if labelled free
            if self.schedule[activity.day][activity.time] == 'Free':
                self.schedule[activity.day][activity.time] = []
            
            # add activity to list
            self.schedule[activity.day][activity.time].append(activity)

        return self.schedule

    def get_malus_points(self, schedule):
        """
        Takes in the student's schedule and calculates their amount of maluspoints.
        Add double bookings! 
        """
        # initialise empty counter for total maluspoints
        self.maluspoints = 0

        # loop over each day
        for day, timeslots in schedule.items():

            # initialise helpers
            occupied_count = 0
            empty_count = 0
            switch = False

            #initialise daily malus counter
            day_empty_slots = 0

            # loop over timeslots
            for slot, status in timeslots.items():
                if status != 'Free' and switch == False and occupied_count == 0:
                    switch = True
                    occupied_count += 1
                    empty_count = 0

                elif status == 'Free' and empty_count > 0:
                    empty_count += 1
                    day_empty_slots += 1

                elif status == 'Free' and switch == True:
                    occupied_count = 0
                    empty_count += 1
                    switch = False
                    day_empty_slots += 1

            # if free slots were at tail end of the day
            if switch == False and day_empty_slots > 0:
                # remove the empty slots counted since last occupied
                day_empty_slots -= empty_count

            # get malus points for the day and add to total
            day_malus = self.maluspoints_converter(day_empty_slots)
            self.maluspoints += day_malus

        return self.maluspoints
    
    def get_free_period_malus_points(self):
        """
        Method that takes a students schedule and calculates the amount of malus points resulting
        from the number of free periods between classes for this specific student
        """
        # intialize maluspoint counter
        free_period_maluspoints = 0

        # loop over all days and respective timeslots
        for day, timeslots in self.schedule.items():
            
            # initialize variables
            occupied_timeslots_indices = []
            free_period_count = 0

            # get list of statuses
            slots = list(timeslots.values())
            
            # loop over all indices and statuses of timeslots
            for i, status in enumerate(slots):

                # obtain indices of all occupied timeslots
                if status != 'Free':
                    occupied_timeslots_indices.append(i)
            
            if occupied_timeslots_indices:

                # obtain indices of first and last occupied timeslots
                first_activity_index = occupied_timeslots_indices[0]
                final_activity_index = occupied_timeslots_indices[-1]

                # obtain number of free timeslots between first and last occupied ones
                for i in range(first_activity_index, final_activity_index + 1):
                    if slots[i] == 'Free':
                        free_period_count += 1
            
            # convert into maluspoints for the day and add to total number
            todays_maluspoints = self.maluspoints_converter(free_period_count)
            free_period_maluspoints += todays_maluspoints

        return free_period_maluspoints

    def get_double_booking_malus_points(self):
        double_booking_maluspoints = 0

        for day, timeslots in self.schedule.items():
            for timeslot, activities in timeslots.items():

                # if activities 
                if activities != 'Free' and len(activities) > 1:
                    double_booking_maluspoints += 1
        
        print(f"{self.name} - Double Booking Malus Points: {double_booking_maluspoints}")
        return double_booking_maluspoints
    
    def maluspoints_converter(self, number_empty_slots: int):
        """
        Converts empty slots of one day into malus points.
        """

        malus = 0
        if number_empty_slots == 1:
            malus = 1
        elif number_empty_slots == 2:
            malus = 3
        elif number_empty_slots > 2:
            # not allowed but for now just make cost very high
            malus = 10
            print(f'{number_empty_slots} empty slots is not allowed! Change algorithm!')

        return malus

    def get_total_maluspoints(self):
        """
        Sets total number of maluspoints --> INCOMPLETE 
        """
        self.maluspoints = self.get_free_period_malus_points() + self.get_double_booking_malus_points()

        return self.maluspoints
