close all;
clear all;
clc;

%Geometry Definition
L = 0.2; %Length of the rod in m
N = 10;  %Number of nodes
dx = L/(N-1);  %Grid size
dt = 5e-3;    %Time step
t_max = 0.3;  %Max simulation time
x = linspace(0,L,N);;
t=0:dt:t_max;

alpha = 0.05;           %DIffusion coefficient

%Intial and Boundary Condtions
Tb = 300;                   %Boundary Condition at base
Ttip = 50;                  %Boundary Condition at tip
Tcurrent = ones(1,N)*30;

%Solution
d = alpha*dt/dx^2;       % value of d should be less than 0.5 for a stable solution

for j = 2:length(t)      % Loop for the timestep   
  T = Tcurrent;
  T(1) = Tb;
  T(end) = Ttip;
  for i = 2:(N-1)
     T(i) = T(i)+d*(T(i+1)-2*T(i)+T(i-1));
  endfor

Tcurrent = T;
time = j*dt;
plot(x,Tcurrent)    
xlabel('Length of the rod','FontSize',14)
ylabel('Temperature in C','FontSize',14)
set(gca,'FontSize',16)
str1 = sprintf('Value of d = %d',d);
str2 = sprintf('Time Value = %d s',time);
text(0.12,150,str1,'FontSize',14)
text(0.12,130,str2,'FontSize',14)
shg
pause(0.01) 
end

