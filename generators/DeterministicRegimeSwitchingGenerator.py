import numpy as np
from generators.Generator import Generator


class DeterministicRegimeSwitchingGenerator(Generator):
    def change_parameters_after_warmup(self):
        self.drift_list = np.array([])
        self.transition_matrix = np.array([])

    def __init__(self, mu_list, transition_matrix, omega0, initial_regime):
        """
        - mu_list: list of deterministic drifts (means) [c_1, c_2, ..., c_M] for each regime
        - transition_matrix: MxM matrix with transition probabilities p_ij
        - omega0: initial log-price (ω₀)
        - initial_regime: initial regime index (0-based)
        """
        self.omega = None
        self.current_regime = None

        self.drift_list = np.array(mu_list)
        self.transition_matrix = np.array(transition_matrix)
        self.omega0 = omega0
        self.initial_regime = initial_regime
        self.M = len(mu_list)
        self.reset()

    def reset(self):
        self.current_regime = self.initial_regime
        self.omega = self.omega0

    def generate(self):
        # Step 1: Sample next regime based on current regime
        self.current_regime = np.random.choice(
            self.M, p=self.transition_matrix[self.current_regime]
        )

        # Step 2: Add deterministic drift based on current regime
        self.omega += self.drift_list[self.current_regime]

        # Return the updated log-price (ω_t)
        return self.omega
