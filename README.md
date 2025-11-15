# Agent-Based-Immune-Modeling

Understanding the dynamics of the immune system's response to infections and the overreactions that can arise are essential to discovering how autoimmune diseases and chronic infammation arise.

In this project, we proceduraly generated a two-dimensional world of healthy, infected, and immune cells. The immune cells are agents governed by a utility function to determine whether to move or attack.
Attacking utility is calculated by summing the number of infected cells immediately neighboring a given immune cell, and subtracting the number of healthy cells. Thus, attacking utility will be positive if they are more infected cells than healthy cells surrounding an immune cell. Moving utility is always between 0 and 1. Thus, an immune cell will always attack if the number of infected cells outnumber the number of healthy cells. Otherwise, it will move.

![cell counts](https://github.com/hayitsian/Agent-Based-Immune-Modeling/blob/main/plots/Cell%20counts%20over%201500%20steps%2050x50%20grid%20InfectProb%3A%200.035%20ReproProb%3A%200.05%20DeathProb%3A%200.03%20AttackSuccess%3A%200.85%20With%20naiveUtility%20immune%20cell%20movement.png)

![cell actions](https://github.com/hayitsian/Agent-Based-Immune-Modeling/blob/main/plots/Cell%20actions%20over%201500%20steps%2050x50%20grid%20InfectProb%3A%200.035%20ReproProb%3A%200.05%20DeathProb%3A%200.03%20AttackSuccess%3A%200.85%20With%20naiveUtility%20immune%20cell%20movement.png)

We found that the immune cells governed by this utility function were capable of erradicating the infection, but quickly outnumbered the number of healthy cells. In other words, the inflammation was to great of a response and did not taper once the infection was contained. Importantly, the resources of the board state (the number of empty spaces) is highly constrained to try and simulate the resource constraints of living beings. Inflammation saps resources that could otherwise be used for homeostatic maintenance.
