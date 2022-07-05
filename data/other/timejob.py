import schedule
import time
import os

def stop_ordering():
    os.system('python3 ./schoollunchweb/manage.py shell < ./stop_ordering.py')

def new_day():
    os.system('python3 ./schoollunchweb/manage.py shell < ./new_day.py')


# set the job doing time
schedule.every().day.at('02:10').do(stop_ordering)
schedule.every().day.at('09:00').do(new_day)

while True:
    schedule.run_pending()
    time.sleep(60)