"""
`every
====================================================

Test whether an interval has gone by:

every_minute = Every(0.5) # every 1/2 second
while (1):
    if every_minute():
        do something

"""

# imports

__version__ = "0.0"

import time

class Every(object):
    """True on every interval"""

    def __init__(self, interval):
        """Make an instance.
           :interval in seconds
        """
        # states are -1,0,1
        self.interval = interval
        self.last = time.monotonic() - interval # start immediatly

    def __call__(self):
        now = time.monotonic()
        diff = now - self.last
        if (diff >= self.interval):
            drift = diff % self.interval
            self.last = now
            self.last -= drift
            return True
        else:
            return False
