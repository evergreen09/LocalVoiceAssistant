from datetime import datetime

time = '21:09'

time_convert = datetime.strptime(time, '%H:%M')

print(time, time_convert)
