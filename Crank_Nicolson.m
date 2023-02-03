close all;
clear all;
clc;
%Geometry Definition
L = 0.2; %Length of the rod in m
N = 20;  %Number of nodes
dx = L/(N-1);  %Grid size
dt = 5e-3;    %Time step
t_max = 0.5;  %Max simulation time
x = linspace(0,L,N); %Node spacing
t=0:dt:t_max;   %time_step array
alpha = 0.05;  %Diffusion coefficient

%Intial and Boundary Condtions
T = zeros(length(t),length(x));
T(:,1) = 300;
T(:,end) = 50;
T(1,2:end-1) = 30;

A = 0.5*alpha*dt/((dx)**2);
B = 1 + alpha*dt/((dx)**2);

%Solution
%Creating a matrix for solving temperature at different nodes (LHS in the matrix equation)
T_array = zeros(N-2,N-2);
for i = 1:N-2
  for j = 1:N-2
    if i==j
      T_array(i,j) = -B;
    endif
    if j== i+1 || j==i-1
      T_array(i,j) = A;
    endif
  endfor
endfor

%Solving nodal temperatures at each time step.
for m = 1:length(t)-1 
  % A constant matrix/array is created for known values in the RHS.
  cons_mat = zeros(N-2,1);
  cons_mat(1) = -T(m,2) - A*(T(m,3)-2*T(m,2)+T(m,1)) - A*T(m,1);
  cons_mat(end) = -T(m,end-1) - A*(T(m,end)-2*T(m,end-1)+T(m,end-2))-A*T(m,end);
  for k = 2:length(cons_mat)-1
    cons_mat(k) = -T(m,k+1) -A*(T(m,k+2)-2*T(m,k+1)+T(m,k));
  end 
  aug_mat = [T_array cons_mat]; %Augmented matrix is created to solve for T

  %%creating an upper triangular matrix by using row operations with 1 along the diagonal
  for j = 1:length(cons_mat)
    k=j+1;
    while k <= length(cons_mat)
      if j>=k
        continue
      endif
      aug_mat(k,:) = aug_mat(k,:)-(aug_mat(k,j)/aug_mat(j,j))*aug_mat(j,:);
      k++;
    end
    aug_mat(j,:) = aug_mat(j,:)/aug_mat(j,j); 
  end

  %Solving for temperature values at a certain time step using Thompson's algorithm
  T_sol = zeros(length(cons_mat),1);
  T_sol(end) = aug_mat(end,end);
  for i = length(cons_mat)-1:-1:1
    T_sol(i)= aug_mat(i,end)-aug_mat(i,i+1)*T_sol(i+1);
  end
  T(m+1,2:end-1) = T_sol;
  % Plotting of temperature values at each time step
  plot(x,T(m,:))    
  xlabel('Length of the rod','FontSize',14)
  ylabel('Temperature in C','FontSize',14)
  set(gca,'FontSize',16)
  str1 = sprintf('Time Value = %d s',t(m));
  text(0.12,130,str1,'FontSize',14)
  shg
  pause(0.01) 
end
disp(T)


