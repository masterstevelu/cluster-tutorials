%{
   This script samples a parameter of a stiff ODE and solves it both in
   serial and parallel (via parfor), comparing both the run times and the
   max absolute values of the computed solutions. The code -- especially the
   serial part -- will take several minutes to run.
%}

% open the local cluster profile
p = parcluster('local');

% open the parallel pool, recording the time it takes
time_pool = tic;
% set the number of parallel CPU cores 
parpool(p, 24);
time_pool = toc(time_pool);
fprintf('Opening the parallel pool took %g seconds.\n', time_pool)

% create vector of random coefficients on the interval [975,1050]
nsamples = 100; % number of samples
coef = 975 + 50*rand(nsamples,1); % randomly generated coefficients

% compute solutions within serial loop
time_ser = tic;
y_ser = cell(nsamples,1); % cell to save the serial solutions
for i = 1:nsamples
  if mod(i,10)==0
    fprintf('Serial for loop, i = %d\n', i);
  end
  [~,y_ser{i}] = ode15s(@(t,y) stiffODEfun(t,y,coef(i)) ,[0 10000],[2 0]);
end
time_ser = toc(time_ser);

% compute solutions within parfor
time_parfor = tic;
y_par = cell(nsamples,1); % cell to save the parallel solutions
err = zeros(nsamples,1); % vector of errors between serial and parallel solutions
parfor i = 1:nsamples
  if mod(i,10)==0
    fprintf('Parfor loop, i = %d\n', i);
  end
  [~,y_par{i}] = ode15s(@(t,y) stiffODEfun(t,y,coef(i)) ,[0 10000],[2 0]);
  err(i) = norm(y_par{i}-y_ser{i}); % error between serial and parallel solutions
end
time_parfor = toc(time_parfor);
time_par = time_parfor + time_pool;

% print results
fprintf('RESULTS\n\n')
fprintf('Serial time : %g\n', time_ser)
fprintf('Parfor time : %g\n', time_par)
fprintf('Speedup : %g\n\n', time_ser/time_par)
fprintf('Max error between serial and parallel solutions = %e\n', max(abs(err)))

% close the parallel pool
delete(gcp)
exit