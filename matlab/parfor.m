% start the matlabpool with 24 workers
pc = parcluster('local')

parpool(pc, 24)

% run a parfor loop, distributing the iterations to 24 workers
parfor i = 1:100
        ones(10,10)
end
