from WarmupGame import WarmupGame
from tqdm import tqdm
import json
from generators.LinearGenerator import LinearGenerator
from generators.NormalDistributionGenerator import NormalDistributionGenerator
from generators.MeanRevertingGBMGenerator import MeanRevertingGBMGenerator
from generators.NoisyRegimeSwitchingGenerator import NoisyRegimeSwitchingGenerator
from generators.RealWorldAssetPriceGenerator import RealWorldAssetPriceGenerator
from generators.SineWaveGenerator import SineWaveGenerator
from generators.DeterministicRegimeSwitchingGenerator import DeterministicRegimeSwitchingGenerator
from strategies.ZeroTradingStrategy import ZeroTradingStrategy
from strategies.BernoulliTradingStrategy import BernoulliTradingStrategy
from strategies.FixedRuleTradingStrategy import FixedRuleTradingStrategy
from strategies.MeanReversionFullTradingStrategy import MeanReversionFullTradingStrategy
from strategies.MeanReversionTimeWindowedTradingStrategy import MeanReversionTimeWindowedTradingStrategy
from strategies.SGDClassifierTradingStrategy import SGDClassifierTradingStrategy
from strategies.ReinforcementLearningTradingStrategy import ReinforcementLearningTradingStrategy
import numpy as np

generators = [
    LinearGenerator(),
    NormalDistributionGenerator(),
    MeanRevertingGBMGenerator(
        dt=1/365,
        mu=np.log(40),
        theta=0.2,
        sigma=0.35,
        omega0=np.log(40)),
    NoisyRegimeSwitchingGenerator(
        mu_list=[0.001, -0.02, 0.02],
        sigma_list=[0.01, 0.1, 0.1],
        transition_matrix=np.array([
            [0.60, 0.20, 0.20],
            [0.15, 0.80, 0.05],
            [0.15, 0.05, 0.80],
        ]),
        initial_regime=0,
        omega0=np.log(40)),
    RealWorldAssetPriceGenerator(),
    SineWaveGenerator(),
    DeterministicRegimeSwitchingGenerator(
        mu_list=[0.001, -0.02, 0.02],
        transition_matrix=np.array([
            [0.60, 0.20, 0.20],
            [0.15, 0.80, 0.05],
            [0.15, 0.05, 0.80],
        ]),
        initial_regime=0,
        omega0=np.log(40)),
]

strategies = [
    BernoulliTradingStrategy(),
    FixedRuleTradingStrategy(),
    MeanReversionFullTradingStrategy(),
    MeanReversionTimeWindowedTradingStrategy(),
    ReinforcementLearningTradingStrategy(),
    SGDClassifierTradingStrategy(),
    ZeroTradingStrategy()
]

# constants
max_simulations = 50
total_movements = 10000


def execute_simulation(number_of_simulations, generator, strategy, num_movements):
    """
    executes a series of game simulations between a generator and an observer.

    parameters:
        number_of_simulations (int): number of simulations to run.
        generator (object): a generator instance
        observer (object): an observer instance
        num_movements (int): number of movements in each game

    returns:
        np.ndarray: array containing scores from all simulations.
    """

    # initialize empty array to keep track of the final scores of the simulations
    scores = np.array([])
    result_tuples = []

    # for each simulation play a game
    for index in tqdm(range(number_of_simulations), desc=f"Simulating {type(generator).__name__} vs {type(strategy).__name__}"):
        game = WarmupGame(generator, strategy, num_movements)

        score = game.play_game()

        # append the score from this simulation to the scores array
        scores = np.append(scores, score)

        result_tuples.append(game.bet_results)

        # reset the generators and strategies
        generator.reset()
        strategy.reset()

    # print(result_tuples)
    return result_tuples


def save_results_to_file(results_from_simulation):
    output = {
        "generator:": type(gen).__name__,
        "strategy": type(strat).__name__,
        "total_movements": total_movements,
        "max_simulations:": max_simulations,
        "simulation": [],
    }

    for sim_index, sim in enumerate(results_from_simulation):
        sim_result = {
            "simulation_number": sim_index,
            "final_score": 0,
            "results": []
        }

        score = 0

        for move_index, (number, bet, correct) in enumerate(sim):
            sim_result["results"].append({
                "number_movement": move_index,
                "generated_number": number,
                "bet": bet,
                "correct_bet": correct
            })
            if correct:
                score += 1
            else:
                score -= 1

        sim_result["final_score"] = score
        output["simulation"].append(sim_result)

    with open(f"simulation_output_{type(gen).__name__}-{type(strat).__name__}.json", "w") as f:
        json.dump(output, f, indent=2)


for gen in generators:
    for strat in strategies:
        results = execute_simulation(max_simulations, gen, strat, total_movements)
        save_results_to_file(results)
