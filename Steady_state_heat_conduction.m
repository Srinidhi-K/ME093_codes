% Matlab code for 1-D steady state heat conduction
clc
close all;
clear all;
%Defining the geometry
L = 10*0.01;  %Length of the rod in m
N = 10:5:20;      %Number of Nodes
% Defining initial and boundary conditions
Tb = 200;            % Boundary condition, base temperature
Ttip=20 ;            % Boundary condition, tip temperature
iter = [];
% Solution
for i=1:length(N)
  T = zeros(N(i),1); 
  dx = L/(N(i)-1);  % Grid size
  T_old = T;
  k=0;      
  err = 100;
  tol = 0.001;
  while true
    T(1,1) = Tb;
    for j = 2:N(i)-1
      T(j,1)= (T(j+1,1)+T(j-1,1))/2; %Temperature inside the domain
    end 
    T(N(i),1) = T(N(i)-1,1);     %Temperature of the last node
    err = abs(max(T-T_old));
    if err < tol
      disp(["For ", num2str(N(i))," nodes Convergence is attained at ", num2str(k),"th iteration"])
      iter = [iter,k];
      break
    endif
    T_old = T;
    figure(i);
    plot(T);   %Plotting T vs node number % If x coordinate is not mentioned, the x-coordinates range from 1 to length(Y).
    title(["Number of nodes = ", num2str(N(i))])
    xlabel("Node number")
    ylabel("Temperature")
    hold on
    k++;
  end
end
hold off
figure(i+1)
plot(N,iter,"-o")
title("Number of nodes vs iteration")
xlabel("Number of nodes")
ylabel("Number of iterations")
