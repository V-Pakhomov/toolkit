import time
import functools
import threading


def time_it(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        start = time.time()
        result = func(*args, **kwargs)

        running_time = time.time() - start
        pretty_running_time = _seconds_to_str(running_time)
        print(f'{func.__name__}() ends with {pretty_running_time}')

        return result

    return wrapper


def time_it_online(func):

    def _online_timer(stop):
        start = time.time()
        while True:

            running_time = round(time.time() - start)
            pretty_running_time = _seconds_to_str(running_time)
            print(f'\r{func.__name__}() is working for {pretty_running_time}', end='')

            if stop():
                print(f'\r{func.__name__}() ends with {pretty_running_time}')
                break

            time.sleep(1)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        stop_timer = False

        timer = threading.Thread(target=_online_timer, args=(lambda: stop_timer,))
        timer.start()

        result = func(*args, **kwargs)

        stop_timer = True
        timer.join()

        return result

    return wrapper


def _seconds_to_str(seconds):

    def time_to_str():
        res_str = ''

        if hours:
            res_str += str(int(hours)) + 'h '

        if minutes:
            res_str += str(int(minutes)) + 'm '

        res_str += str(round(seconds, 3)) + 's'

        return res_str

    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return time_to_str()
