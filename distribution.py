
# If you have a magical power that allows you to teleport anywhere up to a km away, how many times would you need to use the power to get within back_radius?

import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np
import os

SAVE_DIR = "plots"
NUM_SAMPLES = 10000
VALUES = [0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 1, 2, 5, 10, 20, 50, 100]

def walk_in(cur_coords, back_radius, power_radius):
    #You have to go at least once
    iterations = 1
    angle = random.uniform(0, 2*np.pi)
    radius = random.uniform(0, power_radius)
    # Calculate the coordinates
    cur_coords[0] = radius * np.cos(angle)
    cur_coords[1] = radius * np.sin(angle)
    while np.sqrt(cur_coords[0]**2 + cur_coords[1]**2) > back_radius:
        iterations += 1
        angle = random.uniform(0, 2*np.pi)
        radius = random.uniform(0, power_radius)
        # Calculate the coordinates
        cur_coords[0] = radius * np.cos(angle)
        cur_coords[1] = radius * np.sin(angle)
        #print(f"Iteration {iterations}: ({cur_coords[0]}, {cur_coords[1]}) - {np.sqrt(cur_coords[0]**2 + cur_coords[1]**2)}")
    return iterations
def run(power_radius, back_radius):
    in_iters = []
    for i in range(NUM_SAMPLES):
        cur_coords = [0, 0]
        in_iter = walk_in(cur_coords, back_radius, power_radius)
        in_iters.append(in_iter)
        #print(f"Sample {i}: {in_iter} in, {out_iter} out")
    return in_iters
def plot(power_radius, back_radius, in_iters):
    #Plot a histogram of the number of in_iters
    #Custom bins dependent on unique values
    bins = np.arange(0, max(in_iters) + 1.5) - 0.5
    plt.hist(in_iters, bins=bins, density=True, rwidth=0.9, color='blue', alpha=0.5, edgecolor='black', linewidth=1.2)
    plt.title(f"Number of times need to get {back_radius*1000:.0f} m from your power: {power_radius*1000:.0f} m")
    plt.xlabel("Number of iterations")
    plt.ylabel("Frequency")
    #Label the mean
    plt.axvline(np.mean(in_iters), color='green', linestyle='dashed', linewidth=1)
    _, max_ylim = plt.ylim()
    plt.text(np.mean(in_iters)*1.1, max_ylim*0.9, 'Mean: {:.2f}'.format(np.mean(in_iters)), color='green')
    #Label the median
    plt.axvline(np.median(in_iters), color='red', linestyle='dashed', linewidth=1)
    _, max_ylim = plt.ylim()
    plt.text(np.median(in_iters)*1.1, max_ylim*0.8, 'Median: {:.2f}'.format(np.median(in_iters)), color='red' )
    #Label the mode
    plt.axvline(pd.Series(in_iters).mode()[0], color='blue', linestyle='dashed', linewidth=1)
    _, max_ylim = plt.ylim()
    plt.text(pd.Series(in_iters).mode()[0]*1.1, max_ylim*0.7, 'Mode: {:.2f}'.format(pd.Series(in_iters).mode()[0]), color='blue' )
    #Label the max
    plt.axvline(np.max(in_iters), color='orange', linestyle='dashed', linewidth=1)
    _, max_ylim = plt.ylim()
    plt.text(np.max(in_iters)*1.1, max_ylim*0.6, 'Max: {:.2f}'.format(np.max(in_iters)), color='orange' )
    #Label the min
    plt.axvline(np.min(in_iters), color='purple', linestyle='dashed', linewidth=1)
    _, max_ylim = plt.ylim()
    plt.text(np.min(in_iters)*1.1, max_ylim*0.5, 'Min: {:.2f}'.format(np.min(in_iters)), color='purple' )
    #Label the standard deviation below the number of samples
    plt.text(0.95, 0.90, f"std = {np.std(in_iters):.2f}", horizontalalignment='right', verticalalignment='top', transform=plt.gca().transAxes)
    #Label the number of samples - top right
    plt.text(0.95, 0.95, f"N = {NUM_SAMPLES}", horizontalalignment='right', verticalalignment='top', transform=plt.gca().transAxes)
    plt.savefig(os.path.join(SAVE_DIR,f"power_radius_{power_radius}_back_radius_{back_radius}.png"))
    plt.clf()

for power_rad in VALUES:
    for back_rad in VALUES:
        if power_rad <= back_rad:
            continue
        print(f"Power radius: {power_rad}, Back radius: {back_rad}")
        in_iters = run(power_rad, back_rad)
        plot(power_rad, back_rad, in_iters)