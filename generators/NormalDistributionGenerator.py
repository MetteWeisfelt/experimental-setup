from generators.Generator import Generator
import numpy as np


class NormalDistributionGenerator(Generator):
    def change_parameters_after_warmup(self):
        self.__class__.mean = 0
        self.__class__.sigma = 0

    # constants for the normal distribution
    mean = 40
    sigma = 15

    def __init__(self):
        pass

    def reset(self):
        pass

    def generate(self):
        return np.random.normal(self.__class__.mean, self.__class__.sigma)
