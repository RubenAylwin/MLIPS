#!/bin/bash

python runExperiment.py --ips --mlad -L 8 -Y 0.1 -E 0.01 -r 3 -q 2 -g 0.5 --realizations 100 -f E05_Y01_r3_q2
python runExperiment.py --ips --mlad -L 8 -Y 0.1 -E 0.01 -r 3 -q 4 -g 0.5 --realizations 100 -f E05_Y01_r3_q4
python runExperiment.py --ips --mlad -L 8 -Y 0.1 -E 0.01 -r 3 -q 1 -g 0.5 --realizations 100 -f E05_Y01_r3_q1

