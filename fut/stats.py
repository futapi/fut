import datetime
import json
import random
import time

try:  # python2 compatibility
    input = raw_input
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


def calc_next_hour(next_full_hour=False):
    # (don't know which one is better)
    if next_full_hour:  # calculating time until next full hour starts (HH:00)
        t = int(time.time())
        minuite = int(datetime.datetime.fromtimestamp(t).strftime('%M'))
        second = int(datetime.datetime.fromtimestamp(t).strftime('%S'))
        return ((60 - minuite) * 60) + t - second
    else:
        t = time.time()
        return t + 3600  # adding one hour to the current time


def calc_next_day(next_full_day=False):
    # (don't know which one is better)
    if next_full_day:  # calculating time until next day starts (0:00)
        t = int(time.time())
        hour = 24 - int(datetime.datetime.fromtimestamp(t).strftime('%H'))
        minuite = 60 * int(datetime.datetime.fromtimestamp(t).strftime('%M'))
        second = int(datetime.datetime.fromtimestamp(t).strftime('%S'))
        return (3600 * hour) + t - minuite - second
    else:
        t = time.time()
        return t + 3600 * 24  # adding 24 hours to the current time


class Stats:
    stats = None
    file_name = None
    daily_request_limit = hourly_request_limit = None

    def __init__(self, file_name):
        self.file_name = file_name
        self.set_random_daily_request_limit()
        self.set_random_hourly_request_limit()

        try:
            self.stats = json.load(open(file_name))  # loading request count data
            print("Loaded request data, this day: {}/{}, "
                  "this hour: {}/{}".format(self.stats["requests"]["day_count"], self.daily_request_limit,
                                            self.stats["requests"]["hour_count"], self.hourly_request_limit))
        except FileNotFoundError:
            next_hour = calc_next_hour()
            next_day = calc_next_day()
            self.stats = {"requests": {"end_hour": next_hour, "end_day": next_day,
                                       "hour_count": 0, "day_count": 0}}  # creating request count data
            with open(file_name, 'w') as outfile:
                json.dump(self.stats, outfile)
            print("Created stats file")

    def get_next_day(self):
        return self.stats["requests"]["end_day"]

    def get_next_hour(self):
        return self.stats["requests"]["end_hour"]

    def reset_counter(self):
        t = int(time.time())
        day_reset = False
        hour_reset = False
        if t > self.stats["requests"]["end_day"]:  # reset request count data if day has passed
            self.stats["requests"]["end_day"] = calc_next_day()
            self.stats["requests"]["day_count"] = 0
            self.set_random_daily_request_limit()
            day_reset = True
        if t > self.stats["requests"]["end_hour"]:  # reset request count data if hour has passed
            self.stats["requests"]["end_hour"] = calc_next_hour()
            self.stats["requests"]["hour_count"] = 0
            self.set_random_hourly_request_limit()
            hour_reset = True

        return hour_reset, day_reset

    def is_day_request_save(self):
        t = int(time.time())
        return t > self.stats["requests"]["end_day"]

    def is_hour_request_save(self):
        t = int(time.time())
        return t > self.stats["requests"]["end_hour"]

    def is_request_save(self, daily_limit=5000, hourly_limit=500):
        self.reset_counter()

        return self.stats["requests"]["hour_count"] < hourly_limit and \
               self.stats["requests"]["day_count"] < daily_limit

    def get_hourly_requests(self):
        return self.stats["requests"]["hour_count"]

    def get_daily_requests(self):
        return self.stats["requests"]["day_count"]

    def set_random_daily_request_limit(self):
        self.daily_request_limit = random.randint(4800, 5000)

    def set_random_hourly_request_limit(self):
        self.hourly_request_limit = random.randint(470, 500)

    def get_daily_request_limit(self):
        return self.daily_request_limit

    def get_hourly_request_limit(self):
        return self.hourly_request_limit

    def set_daily_request_count(self, value=0):
        self.stats["requests"]["day_count"] = value

    def set_hourly_request_count(self, value=0):
        self.stats["requests"]["hour_count"] = value

    def remove_requests(self, count):
        self.stats["requests"]["day_count"] -= count + 1
        self.stats["requests"]["hour_count"] -= count + 1

        self.save_requests()

    # execution time is about 0.000568 sec (so it should not slow down a bot)
    def save_requests(self, write_file=True, debug=False, increment=1):  # is called every time a request is made
        res = self.reset_counter()
        resetted_hour = res[0]
        resetted_day = res[1]

        self.stats["requests"]["day_count"] += increment
        self.stats["requests"]["hour_count"] += increment

        if debug:
            print("Current request count: {}/{}, {}/{}".format(self.stats["requests"]["hour_count"],
                                                               self.hourly_request_limit,
                                                               self.stats["requests"]["day_count"],
                                                               self.daily_request_limit))

        if write_file:
            with open(self.file_name, 'w') as outfile:
                json.dump(self.stats, outfile)  # save request count data to file

        if not resetted_day:
            if self.get_daily_requests() >= self.daily_request_limit:
                print('script should be paused. did more then {} requests a day.'.format(self.daily_request_limit))

        if not resetted_hour:
            if self.get_hourly_requests() >= self.hourly_request_limit:
                print('script should be paused. did more then {} 500 requests a hour.'.format(
                    self.hourly_request_limit))

    def get_left_hourly_requests(self):
        return self.hourly_request_limit - self.get_hourly_requests()

    def get_left_daily_requests(self):
        return self.daily_request_limit - self.get_daily_requests()

    def reset_day(self):
        self.stats["requests"]["day_count"] = 0

    def reset_hour(self):
        self.stats["requests"]["hour_count"] = 0
