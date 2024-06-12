class Hillclimber():
    def __init__(self, schedule):
        self.final_schedule = schedule
        self.final_maluspoints = schedule.total_maluspoints


    def improve_schedule(self, iters=10):
        """
        Improves the initial schedule for a number of iterations.
        Returns the final schedule when finished.
        """
        # define nr iterations or threshold
        # loop for x iterations or until threshold is reached
            # temp_schedule = switch_course()
            # temp_maluspoints = calculate maluspoints for temp schedule
            # if maluspoints are < than final_maluspoints
                # make this schedule the final schedule
                # make this schedule's maluspoints final maluspoints

        # output final schedule

    
    # IDEA: switch roomslots instead of activities?
    def switch_course(self):
        """
        Switches the room, day, and timeslot of two random activities.
        """
        # loop until switch done successfully:

            # define two activities randomly that are candidates for switching
            # course1 = random choice from schedule.courses
            # course2 = random choice from schedule.courses

            # activity1 = random choice from course1 activities
            # activity2 = random choice from course2 activities

            # if activity2.room > students number in activity1:
                # assign room, day, timeslot of activity1 to activity2
                # assign room, day, timeslot of activity2 to activity1
                # stop looping

        # update rooms with new schedule
        # update students with new schedule
        # update anywhere else where necessary
        # return new schedule
