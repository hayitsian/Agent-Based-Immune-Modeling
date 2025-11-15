#!/usr/bin/env python3

from game import Game
from gamestate import GameState
import random as rand
import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer
from time import sleep
from agents import NaiveUtility, SmartUtility, StupidUtility

def plot(EPOCHS, FIGURE_TITLE, FIGURE_NAME, _labels, data):
    for i in range(len(data)):
        plt.plot(list(range(EPOCHS+1)), data[i], label=_labels[i])

    plt.title(FIGURE_TITLE)
    plt.xlabel("Steps")
    plt.ylabel("# Cells")
    plt.legend()
    plt.savefig(FIGURE_NAME)
    plt.close()


def main(INFECT_PROB = 0.035,
    REPRODUCE_PROB = 0.05,
    DEATH_PROB = 0.03,
    ATTACK_SUCCESS = 0.85,
    IMMUNE_CONSTANT = 0.7,
    HELPER_BOOST = 1.2,
    BOOST_COUNT = 5,
    INIT_CELLS = 20,
    INIT_INFECTED = 4,
    INIT_EFFECTOR = 4,
    INIT_HELPER = 0,
    AUTOCRINE_WINDOW = 1,
    PARACRINE_WINDOW = 2,
    ENDOCRINE_WINDOW = 4,
    WIDTH = 10,
    HEIGHT = 10,
    EPOCHS = 100,
    FRAME_DELAY = 0.1,
    PLOT = True,
    VERBOSE = True
    ):

    INIT_IMMUNE = INIT_EFFECTOR + INIT_HELPER
    INIT_HEALTHY = INIT_CELLS - INIT_IMMUNE - INIT_INFECTED


    gameState = Game.start(WIDTH, HEIGHT, utility=StupidUtility,
                    autocrineWindow = AUTOCRINE_WINDOW, paracrineWindow = PARACRINE_WINDOW, endocrineWindow = ENDOCRINE_WINDOW,
                    infection_prob=INFECT_PROB, repro_prob=REPRODUCE_PROB, die_prob=DEATH_PROB,
                    attack_success=ATTACK_SUCCESS, numCells=INIT_CELLS, 
                    numInfected=INIT_INFECTED, numEffector=INIT_EFFECTOR,
                    numHelper = INIT_HELPER, immune_constant=IMMUNE_CONSTANT,
                    helper_boost=HELPER_BOOST, boost_count=BOOST_COUNT)


    if VERBOSE: print("Initial Conditions:" + "\n" + "Number of healthy Cells: " + str(INIT_HEALTHY) + "\n" + "Number of infected Cells: " 
                      + str(INIT_INFECTED) + "\n" + "Number of immune Cells: " + str(INIT_IMMUNE) + "\n")
    if VERBOSE: print("Grid size: " + str(gameState.width) + "x" + str(gameState.height) + "\n")
    if VERBOSE: print(str(gameState) + "\n", end='\r')

    
    labelsCount = ["Epoch", "Cell count", "Healthy cell count", "Infected cell count", "Immune cell count", "Effector immune cell count", "Helper immune cell count"]
    labelsAction = ["Reproduced cell count", "Moved cell count", "Infected cell count", "Died cell count", "Activated cell count", "Killed cell count"]
    labels = labelsCount+labelsAction

    dataDict = {}
    for _label in labels: 
        dataDict[_label] = []

    dataDict["Epoch"].append(0)
    dataDict["Cell count"].append(INIT_CELLS)
    dataDict["Healthy cell count"].append(INIT_HEALTHY)
    dataDict["Infected cell count"].append(INIT_INFECTED)
    dataDict["Immune cell count"].append(INIT_IMMUNE)
    dataDict["Helper immune cell count"].append(INIT_HELPER)
    dataDict["Effector immune cell count"].append(INIT_EFFECTOR)


    for _label in labelsAction:
        dataDict[_label].append(0)


    startTime = default_timer()

    numSteps = 0

    while numSteps < EPOCHS:

        stepTime = default_timer()
        numSteps += 1

        gameState, data = Game.step(gameState)
        data.insert(0, numSteps)
        dataCount = data[:len(labelsCount)]
        dataAction = data[len(labelsCount):]

        for label, _data in zip(labels, data):
            if VERBOSE: print(f"{label}: {_data}")

        if VERBOSE: print(str(gameState) + "\n", end='\r')

        for label, _data in zip(labels, data):
            dataDict[label].append(_data)

        stepTime = default_timer() - stepTime
        if stepTime < FRAME_DELAY: sleep (FRAME_DELAY - stepTime)

        if not VERBOSE: print(f"Epoch: {numSteps} took {stepTime:.3f} seconds")
        sleep(FRAME_DELAY)

    time = default_timer() - startTime
    # if VERBOSE: print(f"Simulation took: {time:.3f}")
    print(f"Simulation took: {time:.3f}")

    FIGURE_TITLE = f"Cell counts over {EPOCHS} steps {WIDTH}x{HEIGHT} grid\nInfectProb: {INFECT_PROB} ReproProb: {REPRODUCE_PROB} DeathProb: {DEATH_PROB} AttackSuccess: {ATTACK_SUCCESS}\nWith naiveUtility and smart immune cell movement"
    FIGURE_NAME = FIGURE_TITLE.replace("\n", " ") + ".png"

    if PLOT: plot(EPOCHS, FIGURE_TITLE, FIGURE_NAME, labelsCount, [dataDict[_label] for _label in labelsCount])

    FIGURE_TITLE = f"Cell actions over {EPOCHS} steps {WIDTH}x{HEIGHT} grid\nInfectProb: {INFECT_PROB} ReproProb: {REPRODUCE_PROB} DeathProb: {DEATH_PROB} AttackSuccess: {ATTACK_SUCCESS}\nWith naiveUtility and smart immune cell movement"
    FIGURE_NAME = FIGURE_TITLE.replace("\n", " ") + ".png"

    if PLOT: plot(EPOCHS, FIGURE_TITLE, FIGURE_NAME, labelsAction, [dataDict[_label] for _label in labelsAction])


    return np.array(list(dataDict.values())), labels, len(labelsCount)

main()
