#!/bin/bash

#PBS -N matlab_example
### use one node for this job
#PBS -l nodes=1:ppn=1
#PBS -q default

cd $PBS_O_WORKDIR
module load matlab/2016b
matlab -nodisplay -nosplash < matlab_simple.m
