from abc import ABC, abstractmethod


class Generator(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def generate(self):
        pass

    @abstractmethod
    def change_parameters_after_warmup(self):
        pass