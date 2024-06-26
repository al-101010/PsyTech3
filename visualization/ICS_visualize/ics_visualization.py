import pandas as pd
data = pd.read_csv('../../results/hillclimber/tested_hillclimber_output_500K.csv')
group_courses = data.groupby(['Vak', 'Activiteit'])

unique_values = group_courses.agg({
    'Tijdslot': lambda x: x.unique().tolist(),
    'Zaal': lambda x: x.unique().tolist(),
    'Dag': lambda x: x.unique().tolist(),
    'Student': lambda x: x.unique().tolist()
}).reset_index()

def get_start_end_time(timeslot : str):
    if len(str(timeslot)) == 1:
        start_time = '0' + str(timeslot)
    else: 
        start_time = timeslot

    end_time = timeslot + 2

    return start_time, end_time

day_to_date = {'ma' : 24, 'di' : 25, 'wo' : 26, 'do' : 27, 'vr' : 28}

for course in pd.unique(data['Vak']):
    with open(f"{course}.ics", 'w') as f:
        f.write("BEGIN:VCALENDAR\nVERSION:2.0\n")

        for index, row in unique_values.iterrows():
            if course == row['Vak']:
                start_time, end_time = get_start_end_time(row['Tijdslot'][0])

                f.write(f"BEGIN:VEVENT\n")
                f.write(f"SUMMARY:{row['Activiteit']} - {row['Vak']}\n")
                f.write(f"DTSTART;TZID=Europe/Brussels:202406{day_to_date[row['Dag'][0]]}T{start_time}0000\n")
                f.write(f"DTEND;TZID=Europe/Brussels:202406{day_to_date[row['Dag'][0]]}T{end_time}0000\n")
                f.write(f"LOCATION:{row['Zaal'][0]}\n")
                f.write(f"DESCRIPTION:{', '.join(row['Student'])}\n")
                f.write(f"END:VEVENT\n")
        
        f.write('END:VCALENDAR')
        f.close()
