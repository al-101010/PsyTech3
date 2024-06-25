import pandas as pd
import copy

from .student import Student
from .course import Course
from .room import Room
from .activity import Activity


class Schedule:
    """
    A class to represent a schedule.

    . . .

    Attributes
    ----------
    students: list[Student]
        to be scheduled students
    courses: list[Course]
        to be scheduled courses
    rooms: list[Room]
        all rooms 
    activities: list[Activity]
        to be scheduled activities
    roomslots: list[tuple[Room, str, str]]
        all roomslots in the schedule
    archive: list[tupe[Room, str, str]]
        all available roomslots
    room_maluspoints: int
        maluspoints for usage of the evening room slot
    double_booking_maluspoints: int
        maluspoints for students having two activities at the same time
    free_period_maluspoints: int
        maluspoints for (consecutive) free periods
    overcapacity_maluspoints: int
        sum of maluspoints for the amount of student that doesn't fit inside the planned room (capacity of the room)
    total_maluspoints: int
        sum of room, double bookings, free period, and overcapacity maluspoints
    """

    def __init__(self, students_data : str, courses_data : str, rooms_data : str) -> None:
        self.students = self.get_students_list(students_data)
        self.courses = self.get_courses_list(courses_data, self.students)
        self.add_students_courses(self.students, self.courses)
        self.rooms = self.get_rooms_list(rooms_data)
        self.set_largest_room(self.rooms)
        self.activities = self.get_activities_list(self.courses)
        self.roomslots = self.get_room_slots()
        self.archive = copy.copy(self.roomslots)
        
        # initialise all maluspoints 
        self.room_maluspoints = 0
        self.double_booking_maluspoints = 0
        self.free_period_maluspoints = 0  
        self.overcapacity_maluspoints = 0
        self.total_maluspoints = 0

    def is_valid(self) -> bool:
        """
        Returns True if no student in this schedule has 3 free periods 
        in one day (hard constraint).
        """
        # loop over students and check three free periods attribute
        for student in self.schedule.students:
            if student.three_free_periods:
                print(f"Not a valid schedule! {student} has 3 free periods.")
                return False
        
        return True

    def get_students_list(self, data : str) -> list[Student]:
        """
        Iterate through students dataframe and create a Student class for each student.
        Returns a list of students in the form of Student classes.
        """
        # load data
        data = pd.read_csv(data)

        # add students' full name and courses as column
        data['full_name'] = data['Voornaam'] + ' ' + data['Achternaam']
        data['courses'] = data[['Vak1', 'Vak2', 'Vak3', 'Vak4', 'Vak5']].values.tolist()

        students_list = []

        # loop over rows of dataframe and add Student instance to list.
        for index, columns in data.iterrows():
            students_list.append(Student(columns['full_name'], columns['Stud.Nr.'], set(columns['courses'])))

        return students_list

    def get_courses_list(self, data : str, all_students : list[Student]) -> list[Course]:
        """
        Iterate through courses dataframe and create a Course class for each Course.
        Returns a list of courses in the form of Course instances.
        """
        # load data
        data = pd.read_csv(data)

        # initialize list
        courses_list = []

        # loop over rows of dataframe (courses)
        for index, columns in data.iterrows():

            course_students = []

            # loop over all students in any course
            for student in all_students:

                # add student to this course list if they follow the course
                if columns['Vak'] in student.course_names:
                    course_students.append(student)

            # store the number of lectures and their capacity
            lectures = (columns['#Hoorcolleges'], len(course_students))
            tutorials = (columns['#Werkcolleges'], columns['Max. stud. Werkcollege'])
            practicals = (columns['#Practica'], columns['Max. stud. Practicum'])

            # create dictionary of activity types and the amount for this course
            activity_amounts = {'h' : lectures, 'w' : tutorials, 'p' : practicals}

            # add course to courses list
            courses_list.append(Course(columns['Vak'], course_students, activity_amounts))

        return courses_list

    def get_rooms_list(self, data : str) -> list[Room]:
        """
        Iterates through rooms dataframe and creates a Room object for each room.
        Returns a list of Room objects.
        """
        # load data 
        data = pd.read_csv(data)

        # initialize variable
        rooms_list = []

        # loop over rows of dataframe
        for index, columns in data.iterrows():

            # add room info to rooms list
            rooms_list.append(Room(columns['Zaalnummber'], columns['Max. capaciteit']))

        return rooms_list
    
    def set_largest_room(self, rooms : list[Room]) -> None:
        """
        Sets the room with highest capacity as largest room.
        """
        largest_room = sorted(rooms, key=lambda room: room.capacity, reverse=True)[0]
        largest_room.is_largest = True
        largest_room.empty_schedule()
            
    
    def get_activities_list(self, courses : list[Course]) -> list[Activity]:
        """
        Iterates through list of courses and adds their activities to a list, 
        returning said activities list.
        """
        # initialize variable
        activities_list = []

        # loop over courses
        for course in courses:

            # loop over all course activities and add them to list of activities
            for activities in course.activities.values():
                for activity in activities:
                    activities_list.append(activity)

        return activities_list

    def get_room_slots(self) -> list[tuple[Room, str, str]]:
        """
        Return list of all possible roomslots
        """
        # empty list for all room-slots
        room_slots = []

        # add all room-slots to list
        for room in self.rooms:
            for day in room.days:
                for time in room.timeslots:
                    room_slots.append((room, day, time))

        return room_slots

    def add_students_courses(self, students_list : list[Student], courses_list : list[Course]) -> None:
        """
        Add courses to students in the form of Course instances.
        """
        for student in students_list:
            student.add_courses(courses_list)

    def get_evening_room_maluspoints(self) -> int:
        """ 
        Returns malus points for using an evening slot. 
        """
        # reset maluspoints to zero
        self.room_maluspoints = 0

        # loop over all rooms
        for room in self.rooms:

            # loop over all timeslots
            if room.is_largest:
                for timeslots in room.schedule.values():

                    # if largest and evening timeslot is being used, give 5 maluspoints
                    if timeslots.get('17'):
                        self.room_maluspoints += 5 

        return self.room_maluspoints
    
    def get_overcapacity_maluspoints(self) -> int:
        """
        Returns maluspoints for overcapacity (too many students in a room).
        """
        # reset maluspoints
        self.overcapacity_maluspoints = 0
        
        # loop over activities
        for activity in self.activities:

            # for each student in an activity over the room capacity assign 1 point (also to said activity)
            if len(activity.students) > activity.room.capacity:

                # calculate how many students are over capacity
                number_too_many =  len(activity.students) - activity.room.capacity

                # Increase maluspoint counters
                self.overcapacity_maluspoints += number_too_many
                activity.maluspoints += number_too_many

        return self.overcapacity_maluspoints

    def get_student_maluspoints(self) -> tuple[int, int]:
        """
        Get total number of student related maluspoints (double bookings + free periods)
        """
        # reset maluspoints
        self.double_booking_maluspoints = 0
        self.free_period_maluspoints = 0

        # loop over students and collect maluspoints 
        for student in self.students:
            
            # increase maluspoints counters
            self.double_booking_maluspoints += student.get_double_booking_malus_points()
            self.free_period_maluspoints += student.get_free_period_malus_points()
            student.get_total_maluspoints()

        return (self.free_period_maluspoints, self.double_booking_maluspoints)
    
    def reset_maluspoints_activities(self) -> None:
        """
        Resets the maluspoint count for all activities
        """
        for activity in self.activities:
            activity.reset_maluspoints()

    def get_total_maluspoints(self) -> int:
        """
        Returns total amount of maluspoints for this schedule.
        """
        self.reset_maluspoints_activities()
        
        # separate double bookings from free periods 
        student_maluspoints = self.get_student_maluspoints()

        # add all maluspoints together
        self.total_maluspoints = (self.get_evening_room_maluspoints() + 
                                  student_maluspoints[0] + 
                                  student_maluspoints[1] + 
                                  self.get_overcapacity_maluspoints())

        return self.total_maluspoints
    
    def get_output(self, output : str) -> pd.DataFrame:
        """
        Return output schedule as data frame and convert to csv-file 
        with given 'output' name.
        """
        rows = []

        # loop over all activities of each student and append relevant info
        for student in self.students:
            for activity in student.activities:
                
                rows.append([student.name, 
                             activity.course, 
                             activity.name, 
                             activity.room.room_number, 
                             activity.day, 
                             activity.time])

        # create dataframe of schedule
        output_schedule = pd.DataFrame(rows, columns=['Student', 
                                                      'Vak', 
                                                      'Activiteit', 
                                                      'Zaal', 
                                                      'Dag', 
                                                      'Tijdslot'])

        output_schedule.to_csv(output, index=False)

        return output_schedule
