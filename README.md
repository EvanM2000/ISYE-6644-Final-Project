# Riding the Bus in Balatro - A Simulation Project #

**Evan Maurer** | ISYE 6644 - Simulation | Georgia Institute of Technology

## Overview

This project aimed to understand whether common Jokers in Balatro, particularly the common Joker card known as **"Ride The Bus" (RTB)**, and strategies optimized around it were sufficient for beating the game of Balatro. It also tested whether other groups of common Jokers could outperform an RTB-specific strategy.

A variety of comparison tests were run on the data sets produced by each simulated strategy. Thorough analysis of each simulation showed clear and significant differences between strategies.

## Results

- None of the simulated strategies could carry a player to **Ante 8**.
- An **RTB-driven strategy combined with other common Jokers** produced better statistical outcomes than the competing strategies.

## Files

| File | Description |
|---|---|
| `Game_state.py` | The primary mechanism & structure of the simulation, including the logic for how a blind, game, and hand are scored and advanced |
| `Joker.py` | Where all Joker-related logic is created & stored |
| `simulation.py` | Runs the simulation and collects & aggregates the variables of interest |
| `Analysis.ipynb` | Statistical comparison tests on the simulation results, using SciPy & Pandas |

## Notes

- The statistical tests in `Analysis.ipynb` are standard and well documented, so I referenced a few outside sources for how to set them up.
- Most of the print statements in `simulation.py` were written in part with Claude to check that the simulation behaved as expected before running the analysis. The main issue was getting the RTB boolean to pass through correctly and control the simulation. As it turns out, the problem was file naming, not the code itself.

**Tools:** Python, SciPy, Pandas, Jupyter
