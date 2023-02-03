import numpy as np
import math
import xlsxwriter
pin_dia = np.round(np.arange(1.5,4.1,0.1),3) # column 1 pin dia
l_ax = np.round(np.arange(2.5,9.1,0.1),3)    # column 2 l_ax
l_vert = np.round(np.arange(2.5,9.1,0.1),3)  ## column 3 l_vert
height = np.round(np.arange(6.5,7.8,0.1),3)  # column 4 height

l_ax_m = l_ax*0.001
l_vert_m = l_vert*0.001
pin_rad = pin_dia*0.5

length_pin_struct = 110.25
thermal_cond = 237
flow_rate = 12
channel_width = 27.8
surface = round(math.pi*((0.009*0.5)**2),11)

combo = [[i,j,k,l] for i in pin_dia for j in l_ax for k in l_vert for l in height
         if (math.sqrt(j**2+(0.5*k)**2)-i>=1 and k-i>=1)]
for m in combo:
    if m[1]<1.25*m[0] or m[2]<1.25*m[0] or m[1]>2.5*m[0] or m[2]>2.5*m[0]:
        m.insert(4,"Yes")  #column 5 redbox
    else:
        m.insert(4,"No")
    m.insert(5,channel_width*m[3])  #column 6 c/s area
    m.insert(6,round(flow_rate/(60000*m[5]*0.000001),2)) #column 7 flow velocity
    m.insert(7,m[1]/(m[0]*0.5))  #Column 8 L_ax ratio
    m.insert(8,m[2]/(m[0]*0.5))  #column 9 L_vert ratio
    m.insert(9,4*m[1]*m[2]*0.000001)  #column 10 base area(one cell)
    a = (-0.4185-0.5407*0.5*m[0]-0.00356*m[3]-0.06343*m[6]-0.03553*m[7]+0.01622*m[8]-0.000414*thermal_cond
                  +0.14276*0.25*m[0]*m[0]+0.000405*m[3]*m[3]+0.023377*m[6]*m[6]+0.003326*m[7]*m[7]-0.003919*m[8]*m[8]
                  +0.0*thermal_cond*thermal_cond-0.004387*0.5*m[0]*m[3]-0.04191*0.5*m[0]*m[6]-0.00567*0.5*m[0]*m[7]
                  +0.00933*0.5*m[0]*m[8]+0.000039*0.5*m[0]*thermal_cond+0.001302*m[3]*m[6]+0.000128*m[3]*m[7]
                  -0.000023*m[3]*m[8]-0.000012*m[3]*thermal_cond-0.004138*m[6]*m[7]-0.004014*m[6]*m[8]
                  -0.000057*m[6]*thermal_cond-0.000276*m[7]*m[8]+0.000016*m[7]*thermal_cond+0.000034*m[8]*thermal_cond)
    m.insert(10,-(round(np.sign(a)*(np.abs(a))**(-1/0.198732),4)))
    m.insert(11,np.round(1/m[10]/m[9],0))     #HTC_Rth Mean
    m.insert(12,np.round(1/(m[11]*surface),4))    #R_th
    m.insert(13,np.round((2.3958+0.0299*0.5*m[0]-0.00163*m[3]+0.34958*m[6]+0.0038*m[7]-0.47166*m[8]-0.00355*0.25*m[0]*m[0]+0.000177*m[3]*m[3]
                 -0.05174*m[6]*m[6]+0.00271*m[7]*m[7]+0.055283*m[8]*m[8]-0.00115*0.5*m[0]*m[3]+0.01164*0.5*m[0]*m[6]-0.0039*0.5*m[0]*m[7]
                 -0.01405*0.5*m[0]*m[8]+0.000145*m[3]*m[6]-0.000093*m[3]*m[7]-0.000391*m[3]*m[8]+0.0026*m[6]*m[7]-0.01293*m[6]*m[8]
                 -0.00582*m[7]*m[8])**(1/0.0633204),0))
    m.insert(14,np.round(m[13]*length_pin_struct/1000/(0.001*m[1])*0.01,1))

combo.insert(0,["Pin_Dia","L_ax","L_vert","Height","Red_box","Column c/s area","Velocity","L_ax_r","L_vert_r",
                "Base_area","R_th mean","HTC R_th mean","R_th","P_drop_cell","P_drop_cooler"])
workbook = xlsxwriter.Workbook('Cooler_new4.xlsx')
worksheet = workbook.add_worksheet()

col = 0
for row,data in enumerate(combo):
    worksheet.write_row(row,col,data)
workbook.close()
