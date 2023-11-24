# NOTES
# R = F + 459.67



# IMPORT STATEMENTS
import math
import matplotlib.pyplot as plt
import numpy as np



# VARIABLE DEFINITIONS
PIPE_OD = 20 #pipe OD is 20 in
TEMPS_ARR = [800, 900, 1000, 1100] #temperatures of fluid to consider in F
EMISS_SHINY = 0.09 #emissivity for shiny metal like aluminum
EMISS_CLOTH = 0.9 #emissivity for canvas/cloth with matte-black color
PIPE_LEN = 1 #pipe length is 1 ft
TEMP_ENVIRO = 70 #temperature of the surroundings in F
K_INS = 0.05 #thermal conductivity of insulation in BTU/(h*ft*F)
SB_CONST = 0.00000000171 #Stefan-Boltzmann constant in BTU/(h*ft^2*R^4)
INS_THICKNESS_ARR = [2, 3, 4, 5, 6, 7, 8] #insulation thickness cases to consider in inches
SAFETEMP_METAL = 140 #safe-to-touch temperature for shiny metal jacket in F
SAFETEMP_CANVAS = 113 #safe-to-touch temperature for canvas jacket in F
PI = 3.14159



#----------------------------- PART A -------------------------------------------------

#CALCULATION FUNCTION
def calc_surf_temp(emiss, ins, fl_temp):
    #this component of the equation is 0 = coeff_nums[0]*x^4 + coeff_nums[1]*x^3 + coeff_nums[2]*x^2 + coeff_nums[3]*x + coeff_nums[4]
    #where x will be T2
    coeff_nums = [0.0, 0.0, 0.0, 0.0, 0.0]

    #variables
    fluid_temp_F = fl_temp
    pipe_OD = PIPE_OD/12
    ins_thickness = ins/12
    temp_enviro_F = TEMP_ENVIRO
    temp_enviro_R = TEMP_ENVIRO + 459.67

    #calculation
    cond_coeff_list = calc_cond_coeff(K_INS, fluid_temp_F, pipe_OD, (pipe_OD+(2*ins_thickness))) #conduction
    i = 0
    for n in cond_coeff_list:
        coeff_nums[i] += n
        i += 1
    
    conv_coeff = calc_conv_coeff((pipe_OD+(2*ins_thickness))) #convection

    rad_coeff_list = calc_rad_coeff((pipe_OD+(2*ins_thickness)), emiss, SB_CONST, temp_enviro_R) #radiation
    i = 0
    for n in rad_coeff_list:
        coeff_nums[i] += n
        i += 1
    
    #solve the equation
    T2 = solve_eqn(coeff_nums[0], coeff_nums[1], coeff_nums[2], coeff_nums[3], coeff_nums[4], conv_coeff, temp_enviro_F, fluid_temp_F)
    return T2 #return statement

#simple binary search algorithm to solve for the temperature
def solve_eqn(c1, c2, c3, c4, c5, c6, low, high):
    num = 0.0
    T = 0.0
    guessing = True
    counter = 0
    while guessing:
        if (counter == 0): T = (low+high)/2
        num = (c1*math.pow(T,4)) + (c2*math.pow(T,3)) + (c3*math.pow(T,2)) + (c4*T) + c5 + (c6*math.pow((T-70), 1.25))
        if (num > 0): #must decrease T
            high = T
            T = (low+T)/2
        elif (num < 0): #must increase T
            low = T
            T = (high+T)/2
        if (abs(num) <= 0.00001): guessing = False
        counter += 1
    return T


#given k, T1, d1, and d2
#returns a list of two numbers:
#the first number is (-2*k*T1)/(ln(d2/d1))     (note: T1 is in Fahrenheit here)
#the second number is the coefficient for T2, calculated by (2*k)/(ln(d2/d1))
def calc_cond_coeff(k, T1, d1, d2):
    num1 = (-2*k*T1)/math.log(d2/d1)
    num2 = (2*k)/math.log(d2/d1)
    return [0.0, 0.0, 0.0, num2, num1]

#convection portion of the equation is: (0.27)*(d2^0.75)*((T2-T3)^1.25)
#given d2
#returns 0.27*(d2^0.75)
def calc_conv_coeff(d2):
    return 0.27*(math.pow(d2, 0.75))

#given d2, ε, σ, and T3
#returns a list of two numbers:
#the first number is d2*ε*σ, which serves as a coefficient to the T2 quartic expression: (T2^4)+(1838.68*T2^3)+(1267779.053*T2^2)+(388506800*T2)+(459.67^4)
#the second number is d2*ε*σ*(T3)^4    (note: T3 is in Rankine here)
def calc_rad_coeff(d2, e, o, T3):
    num1 = d2*e*o
    num2 = -d2*e*o*math.pow((T3), 4)
    return [num1, (num1*1838.68), (num1*1267779.053), (num1*388506800), ((math.pow(459.67, 4)*num1) + num2)]



#---------------------------- PART B --------------------------------------------

def dataplot():
    #dictionaries where the key is the temp of the fluid in F and the definition is a 2D array of values
    #in this 2D array of values, x is the thickness of calcium silicate (insulation) in inches and y is the surface temp of the jacket in F
    temps_arr = TEMPS_ARR #list of temperatures to use for iterating through the dictionaries

    dict_emiss_shiny = {} #emissivity 0.09 shiny metal jacket
    for p in INS_THICKNESS_ARR:
        for t in temps_arr:
            calcs_arr = []
            count = 0
            for n in INS_THICKNESS_ARR:
                calcs_arr.append(calc_surf_temp(EMISS_SHINY, n, t))
                count += 1
            dict_emiss_shiny[t] = np.array([INS_THICKNESS_ARR,np.array(calcs_arr)])

    dict_emiss_matte = {} #emissivity 0.9 matte black jacket
    for p in INS_THICKNESS_ARR:
        for t in temps_arr:
            calcs_arr = []
            count = 0
            for n in INS_THICKNESS_ARR:
                calcs_arr.append(calc_surf_temp(EMISS_CLOTH, n, t))
                count += 1
            dict_emiss_matte[t] = np.array([INS_THICKNESS_ARR,np.array(calcs_arr)])
    
    #plotting the data:
    plt.figure(figsize=(4.7,8))
    plt.xlim((0,8))

    for t in temps_arr:
        data1 = dict_emiss_shiny[t]
        line1, = plt.plot(data1[0], data1[1], c="b", ls="-", lw=1.5, marker="s", markersize=5)
    line1.set_label("Shiny metal jacket\n(emissivity 0.09)")
    
    for t in temps_arr:
        data2 = dict_emiss_matte[t]
        line2, = plt.plot(data2[0], data2[1], c="r", ls="-", lw=1.5, marker="o", markersize=5)
    line2.set_label("Matte black jacket\n(emissivity 0.9)")

    #plotting 113 F and 140 F lines
    plt.axhline(y=113, color="gray", linestyle="--")
    plt.axhline(y=140, color="gray", linestyle="--")

    #temperature annotations
    #annotations are found by x of the annotation=x-1.25 and y of the annotation=y-2
    for t in temps_arr:
        plt.annotate(str(t) + " F", (INS_THICKNESS_ARR[0]-1.25,dict_emiss_shiny[t][1][0]-2), c="b")
    for t in temps_arr:
        plt.annotate(str(t) + " F", (INS_THICKNESS_ARR[0]-1.25,dict_emiss_matte[t][1][0]-2), c="r")
    plt.annotate("113 F", (0.25, 106), c="gray")
    plt.annotate("140 F", (0.25, 133), c="gray")

    #plot title and x and y labels
    plt.title("Affect of insulation thickness on surface\ntemperature for various emissivities\nand flow temperatures")
    plt.xlabel("Thickness of calcium silicate insulation\non a 20 in diameter pipe (in)")
    plt.ylabel("Surface temperature of jacket (F)")

    #plot
    plt.legend()
    plt.show()



#---------------------------- PART C ------------------------------------------

def barplots():
    temps_arr = TEMPS_ARR #list of temperatures
    
    #dictionaries where the key is the temp of the fluid in F and the definition is a 2D array of values
    #in this 2D array of values, x is the thickness of calcium silicate (insulation) in inches and y is the surface temp of the jacket in F
    dict_emiss_shiny = {} #emissivity 0.09 shiny metal jacket
    for p in INS_THICKNESS_ARR:
        for t in temps_arr:
            calcs_arr = []
            count = 0
            for n in INS_THICKNESS_ARR:
                calcs_arr.append(calc_surf_temp(EMISS_SHINY, n, t))
                count += 1
            dict_emiss_shiny[t] = np.array([INS_THICKNESS_ARR,np.array(calcs_arr)])

    dict_emiss_matte = {} #emissivity 0.9 matte black jacket
    for p in INS_THICKNESS_ARR:
        for t in temps_arr:
            calcs_arr = []
            count = 0
            for n in INS_THICKNESS_ARR:
                calcs_arr.append(calc_surf_temp(EMISS_CLOTH, n, t))
                count += 1
            dict_emiss_matte[t] = np.array([INS_THICKNESS_ARR,np.array(calcs_arr)])

    #explanation here
    temp_dict = {}
    emiss_arr = [EMISS_SHINY, EMISS_CLOTH]
    for t in temps_arr:
        for i in INS_THICKNESS_ARR:
            q_conv_arr = []
            q_rad_arr = []
            for e in emiss_arr:
                outer_temp = calc_surf_temp(e, i, t)
                q_conv = calc_q_conv(outer_temp,i)
                q_rad = calc_q_rad(outer_temp,i,e)
                arr = np.array([q_conv, q_rad, (q_conv + q_rad)])
                b = str(str(t) + "," + str(e) + "," + str(i))
                temp_dict[b] = arr #three values in the array: [q_conv, q_rad, sum]

    #plot data
    for t in temps_arr:
        plt.figure(figsize=(6.5,8))
        x_axis = np.arange(len(INS_THICKNESS_ARR))
        for i in INS_THICKNESS_ARR:
            b1 = str(str(t) + "," + str(emiss_arr[0]) + "," + str(i))
            arr1 = temp_dict[b1]
            b2 = str(str(t) + "," + str(emiss_arr[1]) + "," + str(i))
            arr2 = temp_dict[b2]
            barcolor1, = plt.bar(i-0.2, arr1[2], 0.4, color="b", edgecolor="black", linewidth=1) #q_rad plot for shiny emiss 0.09
            barcolor2, = plt.bar(i-0.2, arr1[0], 0.4, color="r", edgecolor="black", linewidth=1) #q_conv plot for shiny emiss 0.09
            barcolor3, = plt.bar(i+0.2, arr2[2], 0.4, color="green", edgecolor="black", linewidth=1) #q_rad plot for matte emiss 0.9
            barcolor4, = plt.bar(i+0.2, arr2[0], 0.4, color="cyan", edgecolor="black", linewidth=1) #q_conv plot for matte emiss 0.9
            plt.title("Affect of insulation thickness on pipe surface\ntemperature for different emissivities\nat an internal flow temperature of " + str(t) + " F")
            plt.xlabel("Insulation thickness (in)")
            plt.ylabel("Heat rate (BTU/h)")
        barcolor2.set_label("Q_conv for ε = 0.09")
        barcolor1.set_label("Q_rad for ε = 0.09")
        barcolor4.set_label("Q_conv for ε = 0.9")
        barcolor3.set_label("Q_rad for ε = 0.9")
        plt.legend()
        plt.show()



#method to calculate the Q of convection
def calc_q_conv(t, thick):
    d2 = (PIPE_OD/12) + (2*(thick/12))
    return 0.27*PI*(math.pow(d2, 0.75))*(math.pow((t-TEMP_ENVIRO), 1.25))

#method to calculate the Q of radiation
def calc_q_rad(t, thick, emiss):
    d2 = (PIPE_OD/12) + (2*(thick/12))
    return PI*d2*emiss*SB_CONST*((math.pow((t+459.67),4) - math.pow((TEMP_ENVIRO+459.67),4)))



#--------------------------- MAIN METHOD -----------------------------------

def main():
    #PART A
    #specific required calculations for part a
    t1 = calc_surf_temp(EMISS_SHINY, INS_THICKNESS_ARR[0], TEMPS_ARR[3])
    t2 = calc_surf_temp(EMISS_CLOTH, INS_THICKNESS_ARR[0], TEMPS_ARR[3])
    #required print statements for part a
    print("Fluid temperature = " + str(TEMPS_ARR[3]) + " F | Pipe OD = " + str(PIPE_OD) + " in | Insulation thickness " + str(INS_THICKNESS_ARR[0]) + " in = | Jacket emissivity = " + str(EMISS_SHINY) + " | Outer temperature = " + str(round(t1, 2)) + " F\n")
    print("Fluid temperature = " + str(TEMPS_ARR[3]) + " F | Pipe OD = " + str(PIPE_OD) + " in | Insulation thickness " + str(INS_THICKNESS_ARR[0]) + " in = | Jacket emissivity = " + str(EMISS_CLOTH) + " | Outer temperature = " + str(round(t2, 2)) + " F\n")
    
    #PART B
    dataplot()

    #PART C
    barplots()

main()