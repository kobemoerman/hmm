#!/usr/bin/env python3

from player_controller_hmm import PlayerControllerHMMAbstract
from constants import *
import random
from baum_welch import baum_welch, forward_not_normalized, forward
import numpy as np


def almost_uniform(n):
    rnd = []
    for _ in range(0, n):
        rnd.append(random.uniform(0.1, 0.2))
    normalizer = sum(rnd)
    return [r / normalizer for r in rnd]


def stochastic_2(n):
    rnd = []
    for _ in range(0, n):
        rnd.append(random.uniform(0, 100))
    normalizer = sum(rnd)
    return [r / normalizer for r in rnd]


def stochastic(n, m):
    matrix = np.random.rand(n, m)
    return matrix / matrix.sum(axis=1)[:, None]


class HMM:
    def __init__(self):
        # self._A = [stochastic_2(N_SPECIES) for _ in range(0, N_SPECIES)]
        # self._B = [stochastic_2(N_EMISSIONS) for _ in range(0, N_SPECIES)]
        # self._pi = stochastic_2(N_SPECIES)
        self._A = [almost_uniform(N_SPECIES) for _ in range(0, N_SPECIES)]
        self._B = [almost_uniform(N_EMISSIONS) for _ in range(0, N_SPECIES)]
        self._pi = almost_uniform(N_SPECIES)
        # self._A = stochastic(N_SPECIES, N_SPECIES)
        # self._B = stochastic(N_SPECIES, N_EMISSIONS)
        # self._pi = stochastic(1, N_SPECIES)[0]

    def update(self, observations):
        self._A, self._B, self._pi = baum_welch(self._A, self._B, observations, self._pi)

    def get_sim(self, observations):
        return forward_not_normalized(self._A, self._B, observations, self._pi)
        # return forward(self._A, self._B, observations, self._pi)[2]


class PlayerControllerHMM(PlayerControllerHMMAbstract):
    def init_parameters(self):
        """
        In this function you should initialize the parameters you will need,
        such as the initialization of models, or fishes, among others.
        """
        self.models = [HMM() for _ in range(0, N_SPECIES)]
        self.cur_fish_idx = 0
        self.observations = [[] for _ in range(0, N_FISH)]

    def guess(self, step, observations):
        """
        This method gets called on every iteration, providing observations.
        Here the player should process and store this information,
        and optionally make a guess by returning a tuple containing the fish index and the guess.
        :param step: iteration number
        :param observations: a list of N_FISH observations, encoded as integers
        :return: None or a tuple (fish_id, fish_type)
        """

        # This code would make a random guess on each step:
        # return step % N_FISH, random.randint(0, N_SPECIES - 1)

        for i in range(0, N_FISH):
            self.observations[i].append(observations[i])

        # print(step)
        if step < N_STEPS - N_FISH:
            # if step < 10:
            return None

        max_sim = 0
        max_species = 0
        for species in range(0, N_SPECIES):
            sim = self.models[species].get_sim(self.observations[self.cur_fish_idx])
            if sim > max_sim:
                max_sim = sim
                max_species = species

        self.cur_fish_idx += 1
        return self.cur_fish_idx - 1, max_species

    def reveal(self, correct, fish_id, true_type):
        """
        This methods gets called whenever a guess was made.
        It informs the player about the guess result
        and reveals the correct type of that fish.
        :param correct: tells if the guess was correct
        :param fish_id: fish's index
        :param true_type: the correct type of the fish
        :return:
        """
        if not correct:
            self.models[true_type].update(self.observations[fish_id])
