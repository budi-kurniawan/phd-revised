# ACE ZERO RL

This is the RL code that uses acezero to train a fighter aircraft. The ace_zero_core project is a pre-requisite and needs to be referenced from this project.
Viper (blue) is our RL fighter
Cobra (red) is the adversary

You can run it as follows:

    > python main.py

Documentation can be found in:

    docs/_build/index.html

All folders except the ones that start with 'rl' (rl and rl_data) contains the acezero original code/data


List of Agents
RewardShaping: Uses state transition as reward shaping function
RewardShaping2: Uses only dx as reward shaping function (not successful)

# AceZeroCore
The air-combat simulator that can play 1v1 combat between Viper (blue) against Cobra (red). Both Viper and Cobra are fighters
that are instantiated using a scenario (json) file. The scenario file specifies initial conditions for both fighters as well as
agent classes that will be instantiated as pilots.

# Anaconda Python 3.7
After installing Anaconda, install required packages:

> pip install numpy matplotlib seaborn

# OMP_NUM_THREADS
When using Pytorch, set environment variable OMP_NUM_THREADS to 1

> export OMP_NUM_THREADS=1

Calling torch.setNumThreads(1) does not work in Pytorch 1.2 and 1.4

# Known Issues
Some Python installation failed due to missing module numpy.random.generator. 
