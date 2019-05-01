#!/bin/bash

#PBS -N Huitu_parallel
### use one node for this job
#PBS -l nodes=1:ppn=24
#PBS -q default

cd $PBS_O_WORKDIR
### set python in anaconda 
module load anaconda/5.3.0

python3 huitu_parallel.py
