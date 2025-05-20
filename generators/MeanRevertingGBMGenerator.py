import numpy as np
from generators.Generator import Generator


class MeanRevertingGBMGenerator(Generator):
    def change_parameters_after_warmup(self):
        self.mu = 0
        self.theta = 0
        self.sigma = 0
        self.dt = 0

    def reset(self):
        self.omega = self.omega0

    def generate(self):
        eta = np.random.normal()
        self.omega = self.omega + self.theta * (self.mu - self.omega) * self.dt + self.sigma * np.sqrt(self.dt) * eta
        return self.omega

    def __init__(self, mu, theta, sigma, dt, omega0):
        """
        - mu: long-term mean of the process
        - theta: speed of mean reversion
        - sigma: volatility
        - dt: time step size
        - omega0: initial log-price (ω0)
        """
        self.mu = mu
        self.theta = theta
        self.sigma = sigma
        self.dt = dt
        self.omega0 = omega0
        self.omega = omega0
