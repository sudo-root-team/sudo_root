class Lcg(object):
    
    def __init__(self, multiplier, addend, mod, bits_hidden, state=None):
        self.a = multiplier
        self.b = addend
        self.mod = mod
        self.hidder = 1 << bits_hidden
        self.state = state
        
    def get_state(self, r0, r1, r2):
        t = self.hidder * r1 - self.a * self.hidder * r0 - self.b + self.hidder - 1
        t %= self.mod
        
        end = (self.hidder * self.a - 1 - t) / self.mod
        for k in range(1,end):
            h = t + self.mod * k
            if (h % self.a) < self.hidder:
                state = h / self.a + self.hidder * r0
                if ((state * self.a + self.b) % self.mod * self.a + self.b)% self.mod / self.hidder == r2:
                    self.state = state
                    return self.state
        return 0
    
    def next(self):
        self.state = (self.a * self.state + self.b) % self.mod
        return self.state / self.hidder
