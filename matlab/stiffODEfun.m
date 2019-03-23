function dy = stiffODEfun(t,y,c)
  % This is a modified example from MATLAB's documentation at:
  % http://www.mathworks.com/help/matlab/ref/ode15s.html
  % The difference here is that the coefficient c is passed as an argument.
    dy = zeros(2,1);
    dy(1) = y(2);
    dy(2) = c*(1 - y(1)^2)*y(2) - y(1);
end
