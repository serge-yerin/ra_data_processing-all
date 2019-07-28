import datetime
import time

def wait_for_start(time_to_start, precision):
    now = datetime.datetime.now()
    diff = int((time_to_start - now).total_seconds())
    print("  {:02d}:{:02d}:{:02d}: Script will start in {}m {:02d}s...".format(now.hour, now.minute, now.second, int(diff / 60), diff % 60))
    i = 0
    while True:
        now = datetime.datetime.now()
        diff = int((time_to_start - now).total_seconds())
        i = i + 1
        if i >= 10:
            print("  {:02d}:{:02d}:{:02d}: Script will start in {}m {:02d}s...".format(now.hour, now.minute, now.second, int(diff / 60), diff % 60))
            i = 0
        time.sleep(precision)
        if diff <= 1:
            print (' NOW !!!')
            break



if __name__ == '__main__':

    time_to_start = datetime.datetime(2019, 5, 25, 23, 47, 10)
    precision = 1 # in seconds
    wait_for_start(time_to_start, precision)
