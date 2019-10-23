"""Module to break Linear Congruential Generator"""


class Lcg(object):
    """Create LCG with a state to generate some random value,
    or without state to break LCG with 3 consecutive known values.

    Exemple:

    >>> from sudo_root.crypto import lcg
    >>> l = lcg.Lcg(multiplier, addend, mod, bits_hidden)
    >>> state = l.get_state(r0, r1, r2) # this are 3 consecutive output
    >>> l.next() give us the expected output
    """

    def __init__(self, multiplier, addend, mod, bits_hidden, state=None):
        self.a = multiplier
        self.b = addend
        self.mod = mod
        self.hidder = 1 << bits_hidden
        self.state = state

    def get_state(self, r0, r1, r2):
        "break the LCG with 3 consecutive output."
        t = self.hidder * r1 - self.a * self.hidder * \
            r0 - self.b + self.hidder - 1
        t %= self.mod

        end = (self.hidder * self.a - 1 - t) // self.mod
        for k in range(1, end):
            h = t + self.mod * k
            if (h % self.a) < self.hidder:
                state = h // self.a + self.hidder * r0
                if ((state * self.a + self.b) % self.mod * self.a + self.b) \
                        % self.mod // self.hidder == r2:
                    self.state = state
                    return self.state
        return self.state

    def next(self):
        "The next value of the LCG."
        self.state = (self.a * self.state + self.b) % self.mod
        return self.state // self.hidder
