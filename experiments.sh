#!/bin/bash

# This script will execute 5 experiments, 5 runs each. Total runtime 25 minutes.

# Experiment 0: Run with default settings, do this 5 times
rm -rf logs/experiment0
mkdir logs/experiment0
for run in {1..5}
do
	mkdir logs/experiment0/run$run
	python main.py --clock_range 7 --act_range 11 --duration 60 --log_name experiment0/run$run/process >> logs/experiment0/run$run/config
done


# Experiment 1: All clock rates are exactly the same
rm -rf logs/experiment1
mkdir logs/experiment1
for run in {1..5}
do
	mkdir logs/experiment1/run$run
	python main.py --p0_clock $run --p1_clock $run --p2_clock $run --duration 60 --log_name experiment1/run$run/process >> logs/experiment1/run$run/config
done

# Experiment 2: 0, 1 are slow clock rate, 2 is very very fast
rm -rf logs/experiment2
mkdir logs/experiment2
for run in {1..5}
do
	mkdir logs/experiment2/run$run
	python main.py --p0_clock $run --p1_clock $(($run+1)) --p2_clock $(($run+5)) --duration 60 --log_name experiment2/run$run/process >> logs/experiment2/run$run/config
done


# Experiment 3: 0 is slow, 1 and 2 are fast
rm -rf logs/experiment3
mkdir logs/experiment3
for run in {1..5}
do
	mkdir logs/experiment3/run$run
	python main.py --p0_clock $run --p1_clock $(($run+5)) --p2_clock $(($run+7)) --duration 60 --log_name experiment3/run$run/process >> logs/experiment3/run$run/config
done

# Experiment 4: Default clock rates, but super likely to send messages (act_range down to 4)
rm -rf logs/experiment4
mkdir logs/experiment4
for run in {1..5}
do
	mkdir logs/experiment4/run$run
	python main.py --p0_act 4 --p1_act 4 --p2_act 4 --duration 60 --log_name experiment4/run$run/process >> logs/experiment4/run$run/config
done