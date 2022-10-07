import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import Cross_point_ver2 as cross

def print_fig(fig_name, x_chi, H1, H2):
    plt.plot(x_chi, H1, color = 'black', label = 'Chain A')
    plt.plot(x_chi, H2, color = 'red', label = 'Chain B')
    plt.xlabel(r'$T,~K$')
    plt.ylabel(r'$\langle H \rangle$')
    plt.xlim(x_chi[0], x_chi[-1])
    plt.ylim(0.0, max(max(H1), max(H2))*1.05)
    plt.grid()
    point = cross.cross_point(x_chi, H1, H2)
    if point:
        plt.plot(point[0], point[1], c = 'g', marker = 'o', ms=5)       
    plt.legend(frameon=False, fontsize=10)
    plt.draw()
    plt.savefig(fig_name, dpi=300)
    plt.clf()

# def print_derivative(fig_name, x_T, H_derivative):
#     plt.plot(x_T, H_derivative, 'o-r', label = r'$\frac{d(H_1-H_2)}{dT}$')
#     plt.xlabel(r'$T,~K$')
#     plt.ylabel(r'$d(H_1-H_2)$')
#     plt.xlim()
#     plt.ylim()
#     plt.grid()   
#     plt.legend(frameon=False, fontsize=10)
#     plt.draw()
#     plt.savefig(fig_name, dpi=300)
#     plt.clf()

class Flex_api:
    def __init__(self, N1, sigma1, p1, chi1, N2, sigma2, p2, chi2):
        self.N1 = N1 #polymerization degree
        self.sigma1 = sigma1 #grafting density
        self.p1 = p1 #Kuhn length
        self.chi1 = chi1 #Flory's parameter for polymer-solvent
        self.N2 = N2 #polymerization degree
        self.sigma2 = sigma2 #grafting density
        self.p2 = p2 #Kuhn length
        self.chi2 = chi2 #Flory's parameter for polymer-solvent
        self.chi12 = 0.0 #Flory's parameter for polymer-polymer
        self.eta = 0.04 #step size of gradient descent
        self.nfree = 5000 #number of "free steps" at descent
        self.swpro = 1 #if swpro=0: switch off print of profile
    
    def print_input(self):
        with open('INPUT.txt', 'w') as f:
            f.write(f'{self.N1} \n')
            f.write(f'{self.sigma1} \n')
            f.write(f'{self.p1} \n')
            f.write(f'{self.chi1} \n')
            f.write(f'{self.N2} \n')
            f.write(f'{self.sigma2} \n')
            f.write(f'{self.p2} \n')
            f.write(f'{self.chi2} \n')
            f.write(f'{self.chi12} \n')
            f.write(f'{self.eta} \n')
            f.write(f'{self.nfree} \n')
            f.write(f'{self.swpro} \n')
    
    def read_data(self):
        with open('data.out', 'r') as data:
            data.readline()
            st = list(map(float, data.readline().split()))
            H1 = st[0]
            H2 = st[1]
            F = st[2]
        return H1, H2

#Extrapolate function
Temp_value = [280.0, 282.5, 287.5, 292.5, 295.0, 297.5, 307.5, 312.5, 320.0, 322.5]
chi1_T = [1.44, 1.29, 1.0, 0.75, 0.63, 0.5, 0.13, -0.03, -0.188, -0.226]
chi2_T = [-0.6, -0.5, -0.3, -0.102, 0.0, 0.108, 0.5, 0.688, 0.983, 1.08]
chi1_T = interpolate.interp1d(np.array(Temp_value), np.array(chi1_T), kind = 3, fill_value='extrapolate')
chi2_T = interpolate.interp1d(np.array(Temp_value), np.array(chi2_T), kind = 3, fill_value='extrapolate')
#Extrapolate function check
# plt.plot(Temp_value, [float(chi1_T(x)) for x in Temp_value], linewidth= 2, c = 'purple', label = '_ dergee')
# print(float(chi1_T(280)))
# plt.plot(Temp_value, [float(chi2_T(x)) for x in Temp_value], c = 'red')
# plt.legend()
# plt.show()
# print([float(chi1_T(x)) for x in Temp_value])
# print(chi1_T(300))
# exit(0)

flex = Flex_api(100, 0.01, 1.0, 0.0, 100, 0.01, 1.0, 0.25)  #Here we enter values to run Flex_api class. N2 can be any, cause we create a cycle for it
flex.swpro = 0
with open("Data_result.txt", "a") as file:
    for n in [100, 110, 120, 130, 140, 150]:                                         #Enter range of N2 values
        flex.N2 = n
        H1 = []
        H2 = []
        x_T = []
        label = True
        T0 = 275.0
        iter_T = 0
        delta_T = 0.5
        while label:                                        #Cycle for Chi parameter changing
            T = T0 + iter_T * delta_T
            iter_T += 1
        # for chi in np.arange(0.0, 0.4, 0.1):
            flex.chi2 = float(chi2_T(T))
            flex.chi1 = float(chi1_T(T))
            flex.print_input()
            os.system(r'.\flex.exe')
            t1, t2 = flex.read_data()
            H1.append(t1)
            if T > 330.0:
                label = False
            H2.append(t2)
            x_T.append(T)
            #print(T, t1, t2, flex.chi1, flex.chi2)    
        ans = cross.cross_point(x_T, H1, H2)
        #H_derivative = np.gradient([(i - j) / ans[1] for i, j in zip(H1 , H2)]) / np.gradient(x_T)
        #point_der = (abs(min(H2-ans[1]))/ans[1] + abs(min(H1-ans[1]))/ans[1]) * 0,5   
        #H_derivative = np.gradient([(point_der / ans[1])])/ np.gradient(x_T)
        #H_derivative = np.gradient(point_der, x_T, edge_order=2)
        if ans:
            file.write(f'{flex.N2}   {flex.sigma1}   {ans[0]}   {ans[1]} \n')
        else:
            file.write(f'{flex.N2}   {flex.sigma1}   -   - \n')
        print_fig(f'H on T depen, N2={flex.N2}, sigma={flex.sigma2}, 3 dergee.jpg', x_T, H1, H2)
        #print_derivative(f'Derivative graph, N2={flex.N2}, sigma={flex.sigma2}.jpg', x_T, H_derivative)
        
#der_max = Der_func.der_point(x_T, H_derivative)
#print(der_max)
#H_derivative = np.gradient(np.array([i-j for i,j in zip(H1, H2)])/np.gradient(np.array(x_T)))
#