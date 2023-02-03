#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
import math


global pose,e_theta,theta_goal,pub,rate,speed,Kp,dmin,N
e_theta=0.0
theta_goal=0.0
pose=[0,0,0]
PI=3.1415
N = 30


def Waypoints(t):
     x = round(t*2*PI/N,6)
     y = round(2*math.sin(x)*math.sin(x/2),6)
     return [x,y]

def odom_callback(data):
    x = data.pose.pose.orientation.x;
    y = data.pose.pose.orientation.y;
    z = data.pose.pose.orientation.z;
    w = data.pose.pose.orientation.w;
    pose = [round(data.pose.pose.position.x,6), round(data.pose.pose.position.y,6), round(euler_from_quaternion([x,y,z,w])[2],6)]
    
    
def laser_callback(msg):
    global regions
    regions = {
   'bright': min(min(msg.ranges[0:40]),10),
   'fright': min(min(msg.ranges[40:320]),10),
   'front': min(min(msg.ranges[320:400]),10),
   'fleft': min(min(msg.ranges[400:660]),10),
   'bleft': min(min(msg.ranges[679:719]),10),
      }

def go_to_goal(e_theta): 
    speed.linear.x=0.18
    speed.angular.z= -Kp*(e_theta)
    global odp
    odp=pose[2]
    pub.publish(speed)
        
def wall_following():
    dmin=0.7
    if(regions['fleft']<regions['fright']):
        
        while(regions['front']<9.9):
            speed.linear.x=0
            speed.angular.z=0.5
            pub.publish(speed)
            rate.sleep()
        while(regions['fright']<9.9):
            if(math.fabs(pose[2]-odp)<0.1 and regions['front']>9.9):
                break
            speed.linear.x=0.18
            speed.angular.z=Kp*(dmin-regions['fright'])
            pub.publish(speed)
            rate.sleep()
    else:
        while(regions['front']<9.9):
            speed.linear.x=0
            speed.angular.z=-0.5
            pub.publish(speed)
            rate.sleep()
        while(regions['fleft']<9.9):
            if(math.fabs(pose[2]-odp)<0.1 and region['front']>9.9):
                break
            speed.linear.x=0.18
            speed.angular.z=-Kp*(dmin-regions['fleft'])
            pub.publish(speed)
            rate.sleep()


def control_loop():
    global speed,pub,rate
    rospy.init_node('ebot_controller')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/ebot/laser/scan', LaserScan, laser_callback)
    rospy.Subscriber('/odom', Odometry, odom_callback)
    rate = rospy.Rate(10) 
    speed = Twist()
    
    while not rospy.is_shutdown():
        #Tracing the sine curve 
        Kp=5.2
        Kd=1
        x1=0.000
        y1=0.000

        for m in range(1,N+1):
           [x2,y2]= Waypoints(m)
           
           theta_goal = round(math.atan2(y2-y1,x2-x1),6)
           e_theta = round(pose[2]-theta_goal,6)
           pr=0
           
           while(math.fabs(e_theta)>=0.1 or math.fabs(pose[0]-x2)>=0.1 or math.fabs(pose[1]-y2)>=0.1 ):
               e_theta = round(pose[2]-theta_goal,6)
               speed.angular.z = round(-Kp*(e_theta)-Kd*((e_theta-pr)/0.1))
               speed.linear.x = 0.190000
               pub.publish(speed)
               pr=e_theta
               rate.sleep()

           [x1,y1]=[x2,y2] 
        obstacle_avoidance()

def obstacle_avoidance():

    x2=12.5
    y2=0
    dmin = 0.7
    theta_goal = math.atan2(y2-pose[1],x2-pose[0])
    e_theta=pose[2]-theta_goal
    while(math.fabs(pose[1]-y2)> 0.1 or math.fabs(pose[0]-x2)> 0.1):
        if(regions['front']>dmin):
           theta_goal = math.atan2(y2-pose[1],x2-pose[0])
           e_theta=pose[2]-theta_goal
           go_to_goal(e_theta)
        else:
           wall_following()
                    
        rate.sleep()
    speed.linear.x=0
    speed.angular.z=0
    pub.publish(speed)
        
        
if __name__ == '__main__':
    try:
        control_loop()        
    except rospy.ROSInterruptException:
        pass