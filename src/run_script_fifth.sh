#!/bin/bash

python runExperiment.py --ips --mlad --ipsw -L 5 -Y 0.1 -E 0.005 -r 3 -q 2.5 -g 0.5 --realizations 100 -f E.005_Y0.1_r3_q2_g0.5

python runExperiment.py --ips --mlad --ipsw -L 5 -Y 0.1 -E 0.001 -r 3 -q 2.5 -g 0.5 --realizations 100 -f E.001_Y0.1_r3_q2_g0.5

python runExperiment.py --ips --mlad --ipsw -L 5 -Y 0.01 -E 0.0005 -r 3 -q 2.5 -g 0.5 --realizations 100 -f E.0005_Y0.01_r3_q2_g0.5
python runExperiment.py --ips --mlad --ipsw -L 5 -Y 0.01 -E 0.0001 -r 3 -q 2.5 -g 0.5 --realizations 100 -f E.0001_Y0.01_r3_q2_g0.5



