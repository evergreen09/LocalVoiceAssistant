from datetime import datetime 
import threading
import time

class AlarmClock:
    def __init__(self, alarm_time):
        self.alarm_time = alarm_time
        self.alarm_thread = threading.Thread(target=self.run_alarm)

    def run_alarm(self):
        current_time = datetime.now().strftime("%H:%M")
        print(current_time, self.alarm_time)
        while current_time != self.alarm_time:
            current_time = datetime.now().strftime("%H:%M")
            time.sleep(5)
            print(current_time, self.alarm_time)
        print("Time to wake up!")

    def start(self):
        self.alarm_thread.start()


alarm = AlarmClock("17:46")

alarm.start()

key = None

while key != 'exit':
    user_input = input("I am a copy cat. I will repeat whatever you say!")
    print(f"{user_input}")
    key = user_input
