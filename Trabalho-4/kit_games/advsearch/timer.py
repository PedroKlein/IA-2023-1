import threading
import time


class FunctionTimer(object):
    """
    A class that allows a method to be called with a timeout.
    Kudos: https://stackoverflow.com/a/46858494/1251716
    Usage (call function foo with arguments (5,3) and 10 seconds of timeout):
    n = FunctionTimer(foo, (5,3))
    print n.run(10)
    """
    def __init__(self, function, args):
        self.function = function
        self.args = args
        self.answer = None

    def worker(self):
        self.answer = self.function(*self.args)

    def run(self, timeout):
        thread = threading.Thread(target=self.worker)
        thread.start()
        thread.join(timeout)
        return self.answer

