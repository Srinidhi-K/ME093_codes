from matplotlib import pyplot as plt
takeoff_height = 0.61     #take-off height above the ground in m
a = 77.8                  #First Coefficient in the Thrust Equation
b = 2.4                   #Second Coefficient in the Thrust Equation
density = 1.225           #Density of Air in kg/m^3
Cl = [0.4]                #Lift Coefficient
Cd = [0.03]               #Drag Coefficient
span = 1                  #wing span in m
chord = 0.16              #Chord of the wing
S = chord*span            #Wing Planform Area in m^2
mass = 1.5                #mass of the plane in kg
weight = 9.81*mass        #total weight of the plane in N
max_takeoff_dist = 2.4    #maximum take-off distance in m
coeff_friction = 0.04     #coefficient of rolling friction
roll_resistance = 9.81*weight*coeff_friction      #total rolling resistance (lift neglected) in N
v_wind = 0                #Positve if head wind and negative if tail wind
v_h = v_wind              #horizontal velocity in m/s
v_v = 0                   #vertical velocity in m/s
delta_t = 0.1            #time step taken for each loop
t_start = 0
t_end = 12
time_array=[]

def time_array_func(t_start,t_end):
    while t_start<t_end:
        t_start = t_start + delta_t
        time_array.append(round(t_start,2))
    return time_array

#Generate time array
time_array = time_array_func(t_start,t_end)

j=0
k=0
while j<len(Cl) and k<len(Cd):
    x_coordinate = [0]  # Horizontal Distance in m
    y_coordinate = [takeoff_height]  # Vertical Distance in m
    for i in range(len(time_array)-1):
        # if(y_coordinate[i]>=0.00):
            thrust = a - b*v_h    #Thrust as a function of velocity
            drag = 0.5*density*Cd[j]*S*v_h**2    #Drag force
            lift = 0.5*density*Cl[k]*S*v_h**2    #Lift force
            # print('Thrust =',thrust,'Drag =',drag, 'Lift =', lift)
            # For tracking the variation of horizontal distance

            if thrust > drag:
                if x_coordinate[i] < max_takeoff_dist and y_coordinate[i] == takeoff_height:
                    acc_h = (thrust - drag - roll_resistance) / mass     #Acceleration in horizontal direction with rolling resistance
                else:
                    acc_h = (thrust - drag) / mass     #Acceleration in horizontal direction without rolling resistance
                v_h = v_h + acc_h * delta_t
                x_coordinate.append(round(x_coordinate[i] + v_h * delta_t, 2))
            else:
                x_coordinate.append(round(x_coordinate[i] + v_h * delta_t,2))

            # For tracking the variation of the vertical height

            if lift <= weight and x_coordinate[i] <= max_takeoff_dist:
                y_coordinate.append(takeoff_height)
            elif (lift > weight or x_coordinate[i] > max_takeoff_dist) and y_coordinate[i]>=0:
                acc_v = (lift-weight)/mass             #Acceleration in vertical direction
                v_v = v_v + acc_v*delta_t
                y_coordinate.append(round(y_coordinate[i]+v_v*delta_t,2))
            else:
                y_coordinate.append(0.00)

    # time_array_new = time_array[:len(y_coordinate)]
    plt.figure(1)
    plt.plot(x_coordinate,time_array)
    plt.xlim(0.00,91.00)
    plt.ylim(0.00,12.00)
    plt.ylabel('Time (in s)')
    plt.xlabel('Horizontal Distance (in m)')
    plt.grid(True)
    plt.figure(2)
    plt.plot(x_coordinate,y_coordinate)
    plt.xlim(0.00, 7.00)
    plt.ylim(0.00, 7.00)
    plt.xlabel('Horizontal Distance (in m)')
    plt.ylabel('Vertical Height (in m)')
    plt.grid(True)
    x_coordinate.clear()
    y_coordinate.clear()
    j=j+1
    k=k+1
plt.show()
