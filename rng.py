import random
import hashlib
class RNG:
    def __init__(self, seed):
        self.seed = str(seed)
        self.rng = random.Random()
        self.hasher = hashlib.md5()
    
    def randomInt(self, inputs, min, max):
        seed = (self.seed +str(inputs)).encode()
        self.hasher.update(seed)
        self.rng.seed(seed)
        return self.rng.randint(min, max)
    
    def randomFloatOne(self, inputs):
        seed = (self.seed +str(inputs)).encode()
        self.hasher.update(seed)
        self.rng.seed(seed)
        return self.rng.random()
        

rng = RNG(6942069420)


