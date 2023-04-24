#!/usr/bin/env python3
from cell import BaseCell, ImmuneCell, NaiveUtility
from gamestate import GameState
import random as rand

import numpy as np

import main
from joblib import Parallel, delayed

from timeit import default_timer

from scipy.stats import sem

import matplotlib.pyplot as plt


INFECT_PROB = 0.05
REPRODUCE_PROB = 0.09
DEATH_PROB = 0.06
ATTACK_SUCCESS = 0.75
INIT_HEALTHY = 200
INIT_INFECTED = 20
INIT_IMMUNE = 20
WIDTH = 100
HEIGHT = 100
EPOCHS = 500
VERBOSE = False

NUM_SIMS = 10

supercellCount = []
superinfCellCount = []
superimmCellCount = []
superaccImmCellCount = []

startTime = default_timer()

res = Parallel(n_jobs=-3, backend="threading", verbose=50)(delayed(main.main)() for i in range(NUM_SIMS))

for i in range(NUM_SIMS):

    r = res[i]
    cellCount = r[0]
    infCellCount = r[1]
    immCellCount = r[2]
    accImmCellCount = r[3]

    supercellCount.append(cellCount)
    superinfCellCount.append(infCellCount)
    superimmCellCount.append(immCellCount)
    superaccImmCellCount.append(accImmCellCount)

time = default_timer() - startTime
print(f"Simulation took: {time}")

plt.errorbar(list(range(EPOCHS+1)), np.mean(supercellCount, axis=0), yerr=sem(supercellCount), label="Total cell count")
plt.errorbar(list(range(EPOCHS+1)), np.mean(superinfCellCount, axis=0), yerr=sem(superinfCellCount), label="Infected cell count")
plt.errorbar(list(range(EPOCHS+1)), np.mean(superimmCellCount, axis=0), yerr=sem(superimmCellCount), label="Immune cell count")
plt.errorbar(list(range(EPOCHS+1)), np.mean(superaccImmCellCount, axis=0), yerr=sem(superaccImmCellCount), label="Activated Immune cell count")


FIGURE_TITLE = f"Cell counts over {NUM_SIMS} iterations {EPOCHS} steps {WIDTH}x{HEIGHT} grid\nInfectProb: {INFECT_PROB} ReproProb: {REPRODUCE_PROB} DeathProb: {DEATH_PROB} AttackSuccess: {ATTACK_SUCCESS}\nWith randomwalk immune cell movement"
FIGURE_NAME = FIGURE_TITLE.replace("\n", " ") + ".png"


plt.title(FIGURE_TITLE)
plt.xlabel("Steps")
plt.ylabel("Cell count")
plt.legend()
plt.savefig(FIGURE_NAME)

