import random
import hashlib
class RNG:
    def __init__(self, seed):
        self.seed = str(seed)
        self.rng = random.Random()
        self.hasher = hashlib.md5()
    
    def randomInt(self, inputs, min, max):
        seed = (self.seed +str(inputs)).encode()
        seed = quick_hash(seed)
        self.rng.seed(seed)
        return self.rng.randint(min, max)
    
    def randomFloatOne(self, inputs):
        seed = (self.seed + str(inputs)).encode()
        seed = quick_hash(seed)
        self.rng.seed(seed)
        # if inputs[0] == 4 and inputs[1] == 8:
        #     print('hashed value:', seed)
        ran = self.rng.random()
        return ran

def quick_hash(data):
    hash_value = 5381  # Initial hash value (can be any prime number)
    for byte in data:
        hash_value = ((hash_value << 5) + hash_value) + byte  # hash * 33 + byte
    return hash_value & 0xFFFFFFFF 

rng = RNG(6942069420)

if __name__ == '__main__':
    print(rng.randomFloatOne([4,8]))
    print(rng.randomFloatOne([4,8]))
    print(rng.randomFloatOne([4,8]))
    rng.randomFloatOne([4,8])
    rng.randomFloatOne([4,8])
    rng.randomFloatOne([4,8])

