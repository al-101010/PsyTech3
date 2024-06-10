import sequential as seq
import math
import pandas as pd
import random

class Student:

    def __init__(self, name : str, number : str, course_names = set[str]) -> None:
        self.name = name
        self.student_number = number
        self.course_names = course_names
        self.courses = set()
        self.activities = set()
        self.schedule = self.empty_schedule()


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

    def total_maluspoints(self):
        """
        Sets total number of maluspoints --> INCOMPLETE 
        """
        self.maluspoints = self.get_free_period_malus_points() + self.get_double_booking_malus_points()

class Course:

    def __init__(self, name : str, students : list[Student], activity_amounts : dict) -> None:
        self.name = name
        self.students = students
        self.activity_amounts = activity_amounts
        self.activities = {}

        self.add_activities(activity_amounts)


    def __repr__(self) -> str:
        return self.name


    def add_activities(self, activity_amounts : dict[str : int]):
        """
        Add all course activities to a dictionary. Accepts a dictionary
        with activities ('h', 'w', 'p') as keys and an amount as value.
        """
        # loop over all activity types to be created
        for activity_type, (amount, capacity) in activity_amounts.items():
            # do not add activities with 0 amount
            if amount == 0:
                continue

            # lectures do not have a capacity so next line not needed
            if not 'h' in activity_type:

                # calculate how many activities of this type are needed by capacity
                amount = math.ceil(len(self.students) / capacity)

            # loop over number of activities of this type
            for i in range(1, amount + 1):
                name = f'{activity_type}{i}'

                # create dictionary key for this activity type and append activity instance to list
                if activity_type in self.activities:
                    self.activities[activity_type].append(Activity(name, capacity, self))
                else:
                    self.activities[activity_type] = [(Activity(name, capacity, self))]

class Activity:

    def __init__(self, name : str, capacity : str, course : Course) -> None:
        self.name = name
        self.capacity = capacity
        self.course = course
        self.scheduled = False


    def __repr__(self) -> str:
        return f'{self.name} from {self.course}'


    def schedule(self, room, day, time):
        """
        Schedule this activity on the given day and time to given room.
        """
        self.room = room
        self.day = day
        self.time = time
        self.scheduled = True

class Room:

    def __init__(self, room_number : str, capacity : str) -> None:
        self.room_number = room_number
        self.capacity = capacity

        self.empty_schedule()


    def __repr__(self) -> str:
        return self.room_number


    def empty_schedule(self, days : list[str] = ['ma', 'di', 'wo', 'do', 'vr'], timeslots : list[str] = ['9', '11', '13', '15']):
        """
        Create an empty schedule for this room, all timeslots are labeled 'free'.
        """

        # give evening slot to biggest room
        if self.room_number == 'C0.110':
            timeslots.append('17')
        else:
            timeslots = ['9', '11', '13', '15']

        self.schedule = {}

        # loop over each day and create a key
        for day in days:
            self.schedule[day] = {}

            # loop over each time slot and label it 'free'
            for timeslot in timeslots:
                self.schedule[day][timeslot] = 'Free'

class Day:
    pass

class Schedule:

    def __init__(self, students_data : str, courses_data : str, rooms_data : str) -> None:
        self.students = self.get_students_list(students_data)
        self.courses = self.get_courses_list(courses_data, self.students)
        self.rooms = self.get_rooms_list(rooms_data)

        self.add_students_courses(self.students, self.courses)


    def get_students_list(self, data : pd.DataFrame) -> list[Student]:
        """
        Iterate through students dataframe and create a Student class for each student.
        Returns a list of students in the form of Student classes.
        """
        data = pd.read_csv(data)

        # add students' full name and courses as column
        data['full_name'] = data['Voornaam'] + ' ' + data['Achternaam']
        data['courses'] = data[['Vak1', 'Vak2', 'Vak3', 'Vak4', 'Vak5']].values.tolist()

        students_list = []

        # loop over rows of dataframe and add Student class to list.
        for index, columns in data.iterrows():
            students_list.append(Student(columns['full_name'], columns['Stud.Nr.'], set(columns['courses'])))

        return students_list

    def get_courses_list(self, data : pd.DataFrame, all_students : list[Student]) -> list[Course]:
        """
        Iterate through courses dataframe and create a Course class for each Course.
        Returns a list of courses in the form of Course classes.
        """
        data = pd.read_csv(data)

        courses_list = []

        # loop over rows of dataframe (courses)
        for index, columns in data.iterrows():

            course_students = []

            # loop over all students in any course
            for student in all_students:

                # add student to this course list if they follow the course
                if columns['Vak'] in student.course_names:
                    course_students.append(student)

            lectures = (columns['#Hoorcolleges'], math.inf)
            tutorials = (columns['#Werkcolleges'], columns['Max. stud. Werkcollege'])
            practicals = (columns['#Practica'], columns['Max. stud. Practicum'])

            activity_amounts = {'h' : lectures, 'w' : tutorials, 'p' : practicals}

            # add course to courses list
            courses_list.append(Course(columns['Vak'], course_students, activity_amounts))

        return courses_list

    def get_rooms_list(self, data : pd.DataFrame) -> list[Room]:
        data = pd.read_csv(data)

        rooms_list = []
        for index, columns in data.iterrows():
            rooms_list.append(Room(columns['Zaalnummber'], columns['Max. capaciteit']))

        return rooms_list

    def add_students_courses(self, students_list : list[Student], courses_list : list[Course]):
        """
        Add courses to students in the form of Subject classes.
        """
        for student in students_list:
            student.add_courses(courses_list)

class Maluspoints:
    def __init__(self, students: list):
        self.total_maluspoints = 0

        # for now only calculated from empty slots
        self.students_maluspoints(students)
        self.evening_room_maluspoints()

    def students_maluspoints(self, students: list):
        """
        Takes in a list of scheduled students and calculates the total amount
        of maluspoints. Add double bookings!
        """

        # loop over each student
        for student in students:
            # add their maluspoints to the total
            self.total_maluspoints += student.maluspoints

        return self.total_maluspoints

    def evening_room_maluspoints(self):
        """
        Calculates maluspoints for usage of evening slot. Finalize.
        """
        pass
