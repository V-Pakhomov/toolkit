import functools


class call_counter:

    def __init__(self, func):
        self.func = func
        self.calls = 0
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        self.calls += 1
        return self.func(*args, **kwargs)

    def __del__(self):
        print(f'{self.func.__name__}() was called {self.calls} times')
