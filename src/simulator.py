#!/usr/bin/env python3

import numpy as np

import main
from joblib import Parallel, delayed

from timeit import default_timer

from scipy.stats import sem
import numpy as np

import matplotlib.pyplot as plt



def errorPlot(epochs, FIGURE_TITLE, FIGURE_NAME, _labels, data):

    for i in range(len(_labels)):
        plt.errorbar(epochs, np.mean(data[i], axis=0), yerr=sem(data[i]), label=_labels[i])

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
params["IMMUNE_CONSTANT"] = 0.7
params["HELPER_BOOST"] = 1.2
params["INIT_HEALTHY"] = 26
params["INIT_INFECTED"] = 8
params["INIT_IMMUNE"] = 8
params["INIT_HELPER"] = 8
params["WIDTH"] = 50
params["HEIGHT"] = 50
params["EPOCHS"] = 1500
params["PLOT"] = False
params["VERBOSE"] = False

NUM_SIMS = 30

supercellCount = []
superinfCellCount = []
superimmCellCount = []
superaccImmCellCount = []
superHealthyCellCount = []

startTime = default_timer()

res = Parallel(n_jobs=-3, backend="multiprocessing", verbose=50)(delayed(main.main)() for i in range(NUM_SIMS))

data_0, labels, numCount = res[0]
data = np.array(res, dtype=object)[:,0]


dataCounts = [_data[1:numCount] for _data in data]
dataActions = [_data[numCount:] for _data in data]



labelCounts = labels[1:numCount]
labelActions = labels[numCount:]


time = default_timer() - startTime
print(f"Simulation took: {time}")


FIGURE_TITLE = f"Cell counts over {NUM_SIMS} iterations {params['EPOCHS']} steps {params['WIDTH']}x{params['HEIGHT']} grid\nInfectProb: {params['INFECT_PROB']} ReproProb: {params['REPRODUCE_PROB']} DeathProb: {params['DEATH_PROB']} AttackSuccess: {params['ATTACK_SUCCESS']}\nWith naiveUtility and smart immune cell movement"
FIGURE_NAME = FIGURE_TITLE.replace("\n", " ") + ".png"

errorPlot(data_0[0], FIGURE_TITLE, FIGURE_NAME, labelCounts, dataCounts)


FIGURE_TITLE = f"Cell actions over {NUM_SIMS} iterations {params['EPOCHS']} steps {params['WIDTH']}x{params['HEIGHT']} grid\nInfectProb: {params['INFECT_PROB']} ReproProb: {params['REPRODUCE_PROB']} DeathProb: {params['DEATH_PROB']} AttackSuccess: {params['ATTACK_SUCCESS']}\nWith naiveUtility and smart immune cell movement"
FIGURE_NAME = FIGURE_TITLE.replace("\n", " ") + ".png"

errorPlot(data_0[0], FIGURE_TITLE, FIGURE_NAME, labelActions, dataActions)


