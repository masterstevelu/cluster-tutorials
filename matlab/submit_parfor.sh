#!/bin/bash

#PBS -N matlab_parfor
### use one node with 24 cores for this job
#PBS -l nodes=1:ppn=24
#PBS -q default

BASE_MFILE_NAME=simple_parfor
MATLAB_OUTPUT=${BASE_MFILE_NAME}.out

cd $PBS_O_WORKDIR
# create a temporary dir for your parallel job
mkdir -p $PBS_JOBID
module load matlab/2016b
matlab -nodisplay -r $BASE_MFILE_NAME > $MATLAB_OUTPUT

# clean up the temporary dir you just created before
rm -rf $PBS_JOBID
