import numpy as np
from generators.Generator import Generator


class NoisyRegimeSwitchingGenerator(Generator):
    def change_parameters_after_warmup(self):
        self.mu_list = np.array([])
        self.sigma_list = np.array([])
        self.transition_matrix = np.array([])

    def __init__(self, mu_list, sigma_list, transition_matrix, omega0, initial_regime):
        """
        - mu_list: list of means [μ₁, μ₂, ..., μ_M] for each regime
        - sigma_list: list of std deviations [σ₁, σ₂, ..., σ_M] for each regime
        - transition_matrix: MxM matrix where element (i,j) is P(m_{t+1}=j | m_t=i)
        - omega0: initial log-price ω₀
        - initial_regime: initial regime index (0-based)
        """

        """
        mu_list = [0.001, -0.02, 0.02]
        sigma_list = [0.01, 0.1, 0.1]

        transition_matrix = np.array([
            [0.60, 0.20, 0.20],  
            [0.15, 0.80, 0.05],  
            [0.15, 0.05, 0.80],  
        ])
        """

        self.mu_list = mu_list
        self.sigma_list = sigma_list
        self.transition_matrix = transition_matrix
        self.omega0 = omega0
        self.initial_regime = initial_regime
        self.m = None
        self.omega = None

        self.M = len(mu_list)
        self.reset()

    def reset(self):
        self.omega = self.omega0
        self.m = self.initial_regime

    def generate(self):
        # Step (a): sample next regime based on current regime
        self.m = np.random.choice(
            self.M, p=self.transition_matrix[self.m]
        )

        # Step (b): generate Gaussian noise with regime-dependent parameters
        eta = np.random.normal(loc=self.mu_list[self.m], scale=self.sigma_list[self.m])

        # Step (c): update log-price
        self.omega += eta

        # Return actual asset price
        return np.exp(self.omega)
