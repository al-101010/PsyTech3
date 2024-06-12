# make class Hillclimber(takes a random schedule?)
# self.final_schedule = get a random schedule
# self.final_maluspoints = get maluspoints of random schedule


# define method to get the final schedule
# define nr iterations or threshold
# loop for x iterations or until threshold is reached
    # temp_schedule = replace a random activity in schedule to different slot (call method below)
    # temp_maluspoints = calculate maluspoints for temp schedule
    # if maluspoints are < than final_maluspoints
        # make this schedule the final schedule
        # make this schedule's maluspoints final maluspoints

# output final schedule and maluspoints


# define method to replace room for activity (takes a schedule)
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
