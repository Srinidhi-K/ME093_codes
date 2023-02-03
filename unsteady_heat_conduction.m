close all;
clear all;
clc;

%Geometry Definition
L = 0.2; %Length of the rod in m
N = 10:2:50;  %Number of nodes
alpha = 0.05;           %Diffusion coefficient
d = 0.1:0.05:0.5; %d = alpha*dt/dx^2; Value of d should be less than 0.5 for a stable solution

%Intial and Boundary Condtions
Tb = 300;                   %Boundary Condition at base
Ttip = 50;                  %Boundary Condition at tip
tol = 0.001;   %tolerance value for error
dx_f=L./(N-1); dt_f=[]; time_f=[]; %Declaring arrays/matrices for plotting

%Solution
for l = 1:length(d)   %loop for different values of d
  for k = 1:length(N)   % loop for different grid size
    dx = L/(N(k)-1);
    dt = d(l)*(dx^2)/alpha;  %time step for a given grid size and d value.
    Tcurrent = ones(1,N(k))*30;   %Initial condition
    j=1;
    time =0;    
    while true
        T = Tcurrent;
        T(1) = Tb;
        T(end) = Ttip;
        for i = 2:(N(k)-1)
          T(i) = T(i)+d(l)*(T(i+1)-2*T(i)+T(i-1));
        endfor
        err = max(abs(Tcurrent - T));
        Tcurrent = T;
        time = j*dt;
        j++;
        if err < tol      %Check for convergence to a steady state.
          disp(["Steady State time = ", num2str(time), " for grid size ", num2str(dx)," and timestep = ", num2str(dt), " d =", num2str(d(l))])
          dt_f(k,l) = dt;
          time_f(k,l) = time;          
          break
        endif
    end
  end
end

figure(1) %Plots the variation fo timestep w.r.t grid size and d.
surf(d,dx_f,time_f);
xlabel('d');
ylabel('dx');
zlabel('time_f');

figure(2) %Plots the variation fo simulation time w.r.t grid size and d.
surf(d,dx_f,dt_f);
xlabel('d');
ylabel('dx');
zlabel('dt');


