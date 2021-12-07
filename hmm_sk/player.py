#!/usr/bin/env python3

import hmm
import random
from player_controller_hmm import PlayerControllerHMMAbstract
from constants import *

import numpy as np

class HMM:
    def __init__(self, fish_types, emission):
        self.A = self.stochastic(fish_types, fish_types)
        self.B = self.stochastic(fish_types, emission)
        self.pi = self.stochastic(1, fish_types)[0]

    def update(self, A, B, pi):
        self.A = A
        self.B = B
        self.pi = pi

    def stochastic(self, n, m):
        matrix = np.random.rand(n, m)
        return matrix / matrix.sum(axis=1)[:, None]

class PlayerControllerHMM(PlayerControllerHMMAbstract):
    def init_parameters(self):
        """
        In this function you should initialize the parameters you will need,
        such as the initialization of models, or fishes, among others.
        """
        self.models = []
        self.fish_obv = []

        for i in range(N_SPECIES):
            self.models.append(HMM(N_SPECIES, N_EMISSIONS))

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
        # return (step % N_FISH, random.randint(0, N_SPECIES - 1))

        return None

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
            self.train_model(true_type)

    def train_model(self, fish_type):
        """
        We train the model again if the fish type is not correct.
        """
        m = self.models[fish_type]

        A, B, pi = hmm.baum_welch(m.A, m.B, self.fish_obv, m.pi)

        HMM.update(A, B, pi)
