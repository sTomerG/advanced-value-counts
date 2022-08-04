from functools import wraps

def check_positive_value(method):
    def inner(self):
        if self.