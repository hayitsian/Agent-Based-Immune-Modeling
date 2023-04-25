#!/usr/bin/env python3
from cell import BaseCell, ImmuneCell, NaiveUtility
from gamestate import GameState
import random as rand

import numpy as np

import main
from joblib import Parallel, delayed

from timeit import default_timer

from scipy.stats import sem
import numpy as np

import matplotlib.pyplot as plt



def errorPlot(EPOCHS, FIGURE_TITLE, FIGURE_NAME, _labels, data):
    for i in range(len(data)):
        plt.errorbar(list(range(EPOCHS+1)), np.mean(data[i], axis=0), yerr=sem(data[i]), label=_labels[i])

    plt.title(FIGURE_TITLE)
    plt.xlabel("Steps")
    plt.ylabel("# Cells")
    plt.legend()
    plt.savefig(FIGURE_NAME)
    plt.close()



params = {}
params["INFECT_PROB"] = 0.035
params["REPRODUCE_PROB"] = 0.05
params["DEATH_PROB"] = 0.03
params["ATTACK_SUCCESS"] = 0.85
params["IMMUNE_CONSTANT"] = 0.95
params["HELPER_BOOST"] = 1.2
params["INIT_HEALTHY"] = 150
params["INIT_INFECTED"] = 20
params["INIT_IMMUNE"] = 20
params["INIT_HELPER"] = 20
params["WIDTH"] = 150
params["HEIGHT"] = 150
params["EPOCHS"] = 1500
params["PLOT"] = False
params["VERBOSE"] = False

NUM_SIMS = 10

supercellCount = []
superinfCellCount = []
superimmCellCount = []
superaccImmCellCount = []
superHealthyCellCount = []

startTime = default_timer()

res = Parallel(n_jobs=-3, backend="threading", verbose=50)(delayed(main.main)() for i in range(NUM_SIMS))

result = np.array(res)

data = []

for i in range(result.shape[1]):
    data.append(result[:,i])

dataCounts = data[0:6]
dataActions = data[6:]

countsLabels = ["Total cell count", "Infected cell count", "Immune cell count", "Healthy cell count", "Helper cell count", "Effector cell count"]
actionsLabels = ["Activated cell count", "Reproduced cell count", "Moved cell count", "Infected cell count", "Died cell count", "Killed cell count", "Boosted cell count", "Suppressed cell count"]

time = default_timer() - startTime
print(f"Simulation took: {time}")

FIGURE_TITLE = f"Cell counts over {NUM_SIMS} iterations {params['EPOCHS']} steps {params['WIDTH']}x{params['HEIGHT']} grid\nInfectProb: {params['INFECT_PROB']} ReproProb: {params['REPRODUCE_PROB']} DeathProb: {params['DEATH_PROB']} AttackSuccess: {params['ATTACK_SUCCESS']}\nWith smartUtility immune cell movement"
FIGURE_NAME = FIGURE_TITLE.replace("\n", " ") + ".png"

errorPlot(params["EPOCHS"], FIGURE_TITLE, FIGURE_NAME, countsLabels, dataCounts)

FIGURE_TITLE = f"Cell actions over {NUM_SIMS} iterations {params['EPOCHS']} steps {params['WIDTH']}x{params['HEIGHT']} grid\nInfectProb: {params['INFECT_PROB']} ReproProb: {params['REPRODUCE_PROB']} DeathProb: {params['DEATH_PROB']} AttackSuccess: {params['ATTACK_SUCCESS']}\nWith smartUtility immune cell movement"
FIGURE_NAME = FIGURE_TITLE.replace("\n", " ") + ".png"

errorPlot(params["EPOCHS"], FIGURE_TITLE, FIGURE_NAME, actionsLabels, dataActions)


