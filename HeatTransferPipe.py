# NOTES
# R = F + 459.67



# IMPORT STATEMENTS
import math



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



#----------------------------- PART A -------------------------------------------------

#CALCULATION FUNCTION
def calc_surf_temp(emiss):
    #this component of the equation is 0 = coeff_nums[0]*x^4 + coeff_nums[1]*x^3 + coeff_nums[2]*x^2 + coeff_nums[3]*x + coeff_nums[4]
    #where x will be T2
    coeff_nums = [0.0, 0.0, 0.0, 0.0, 0.0]

    #variables
    fluid_temp_F = TEMPS_ARR[3]
    pipe_OD = PIPE_OD/12
    ins_thickness = INS_THICKNESS_ARR[0]/12
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
    #debug print out the equation: print(str(coeff_nums[0]) + "*T^4 + " + str(coeff_nums[1]) + "*T^3 + " + str(coeff_nums[2]) + "*T^2 + " + str(coeff_nums[3]) + "*T + " + str(coeff_nums[4]) + " + " + str(conv_coeff) + "*((T-70)^1.25) = 0")
    T2 = solve_eqn(coeff_nums[0], coeff_nums[1], coeff_nums[2], coeff_nums[3], coeff_nums[4], conv_coeff, temp_enviro_F, fluid_temp_F)
    print("Fluid temperature = " + str(fluid_temp_F) + " F | Pipe OD = " + str(PIPE_OD) + " in = " + str(round(pipe_OD, 2)) + " ft | Insulation thickness " + str(INS_THICKNESS_ARR[0]) + " in = " + str(round(ins_thickness, 2)) + " ft | Jacket emissivity = " + str(emiss) + " | Outer temperature = " + str(round(T2, 2)) + " F") 


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




#---------------------------- PART C ------------------------------------------




#--------------------------- MAIN METHOD -----------------------------------

def main():
    #PART A
    calc_surf_temp(EMISS_SHINY)
    calc_surf_temp(EMISS_CLOTH)

    #PART B

    #PART C

main()