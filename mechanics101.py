from matplotlib import pyplot as plt
sample_time = [0]         #Time in seconds
x_coordinate = [0]        #Horizontal Distance in m
y_coordinate = [0.61]     #Vertical Distance in m
a = 137.8                  #First Coefficient in the Thrust Equation
b = 2.4                   #Second Coefficient in the Thrust Equation
density = 1.225           #Density of Air in kg/m^3
Cl = 0.5                  #Lift Coefficient
Cd = 0.1                  #Drag Coefficient
S = 0.16                  #Wing Planform Area in m^2
mass = 1.5                #mass of the plane in kg
weight = 9.81*mass        #total weight of the plane in N
max_takeoff_dist = 2.4    #maximum take-off distance in m
takeoff_height = 0.61     #take-off height above the ground in m
coeff_friction = 0.04     #coefficient of rolling friction
roll_resistance = 9.81*weight*coeff_friction      #total rolling resistance (lift neglected) in N
v_wind = 0                #Positve if head wind and negative if tail wind
v_h = v_wind              #horizontal velocity in m/s
v_v = 0                   #vertical velocity in m/s
delta_t = 0.1            #time step taken for each loop
for i in range(20):
    sample_time.append(round(sample_time[i]+delta_t,2))    #Array of time samples
    thrust = a - b*v_h    #Thrust as a function of velocity
    drag = 0.5*density*Cl*S*v_h**2    #Drag force
    lift = 0.5*density*Cl*S*v_h**2    #Lift force

    # For tracking the variation of horizontal distance

    if thrust > drag:
        if x_coordinate[i] < max_takeoff_dist and y_coordinate[i] == 0.61:
            acc_h = (thrust - drag - roll_resistance) / mass   #Acceleration in horizontal direction with rolling resistance
        else:
            acc_h = (thrust - drag) / mass    #Acceleration in horizontal direction without rolling resistance
        v_h = v_h + acc_h * delta_t
        x_coordinate.append(round(x_coordinate[i] + v_h * delta_t, 2))
    else:
        x_coordinate.append(round(x_coordinate[i] + v_h * delta_t, 2))

    # For tracking the variation of the vertical height

    if lift <= weight and x_coordinate[i] <= max_takeoff_dist:
        y_coordinate.append(takeoff_height)
    elif (lift > weight or x_coordinate[i] > max_takeoff_dist) and y_coordinate[i]>=0:
        acc_v = (lift-weight)/mass    #Acceleration in vertical direction
        v_v = v_v + acc_v*delta_t
        y_coordinate.append(round(y_coordinate[i]+v_v*delta_t,2))
    else:
        y_coordinate.append(0.00)

plt.figure(1)
plt.plot(sample_time,x_coordinate)
plt.xlabel('Time (in s)')
plt.ylabel('Horizontal Distance (in m)')
plt.figure(2)
plt.plot(x_coordinate,y_coordinate)
plt.xlabel('Horizontal Distance (in m)')
plt.ylabel('Vertical Height (in m)')
plt.show()
