% start the matlabpool with maximum available workers
% control how many workers by setting cores in your submit job script
pc = parcluster('local')

% explicitly set the JobStorageLocation to the temp directory that was created in your submit job script
pc.JobStorageLocation = getenv('PBS_JOBID')

parpool(pc, 24)

% run a parfor loop, distributing the iterations to the SLURM_CPUS_ON_NODE workers
parfor i = 1:100

        ones(10,10)

end
