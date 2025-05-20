from generators.Generator import Generator


class LinearGenerator(Generator):
    def change_parameters_after_warmup(self):
        pass

    def __init__(self):
        self.initial_value = 0
        self.current_value = self.initial_value

    def reset(self):
        self.initial_value = 0
        self.current_value = self.initial_value

    def generate(self):
        self.current_value += 1
        return self.current_value

