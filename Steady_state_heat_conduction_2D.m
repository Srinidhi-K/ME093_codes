clear all;
close all;
clc;

%Geometry
L = 10e-2;
H = 10e-2;

%Mesh: Number of nodes
nx = 10;
ny = 10;

x=linspace(0,L,nx);
y=linspace(0,H,ny);
dx=L/(nx-1);
dy=H/(ny-1);

%Initialisation of Temperatures(intial guess values)
T=zeros(nx,ny);

%Boundary Conditions
T(:,1)=20;
T(1,:)=200;
T(:,end)=100;
T(end,:)= 50;
T_old = T;

beta=(dx/dy)^2;
err=200;
tol=1e-3;
k=0;
while err>tol
  k=k+1;
  for i=2:nx-1
    for j=2:ny-1
      T(i,j)=(1/(2+(1+beta)))*(T(i+1,j)+T(i-1,j)+(beta*(T(i,j+1)+T(i,j-1))));
    endfor
  endfor
err = abs(max(max(T-T_old)));
err_p(k)=err;
T_old=T;
end

figure(1)
plot(err_p);
xlabel('No of iterations','FontSize',14)
ylabel('Error/Residual (-)','FontSize',14)
set(gca,'FontSize',16)

figure(2)
contourf(x,y,T,'ShowText','on')
xlabel('Length [m]','FontSize',14)
ylabel('Height [m]','FontSize',14)
title('2D Steady State Heat Conduction','FontSize',16)
set(gca,'FontSize',16)