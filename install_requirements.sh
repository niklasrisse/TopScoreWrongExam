#!/usr/bin/env bash

conda create --name PerfectScore python=3.9.16
eval "$(conda shell.bash hook)"
conda activate PerfectScore

pip install -r ./requirements.txt