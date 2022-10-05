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
T2 = [280.0, 282.5, 295.0, 320.0]
chi2_T = [-0.6, -0.5, 0.0, 1.0]
chi2_T = interpolate.interp1d(np.array(T2), np.array(chi2_T), kind = 2, fill_value='extrapolate')
T1 = [287.5, 292.5, 297.5,  302.9, 312.5, 322.5]
chi1_T  = [1.0, 0.75, 0.5, 0.3, 0.0, -0.25]
chi1_T = interpolate.interp1d(np.array(T1), np.array(chi1_T), kind = 2, fill_value='extrapolate')
#Extrapolate function check
# plt.plot(T1, [float(chi1_T(x)) for x in T1], c = 'blue')
# print(float(chi1_T(280)))
# plt.plot(T2, [float(chi2_T(x)) for x in T2], c = 'red')
# plt.show()
# print([float(chi1_T(x)) for x in T1])
# #print(chi1_T(300))
# exit(0)

flex = Flex_api(100, 0.01, 1.0, 0.0, 110, 0.01, 5.0, 0.25)  #Here we enter values to run Flex_api class. N2 can be any, cause we create a cycle for it
flex.swpro = 0
with open("Chi_data_result.txt", "a") as file:
    for n in [100]:                                         #Enter range of N2 values
        flex.N2 = n
        H1 = []
        H2 = []
        x_T = []
        label = True
        T0 = 275.0
        iter_T = 0
        delta_T = 2.5
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
            print(T, t1, t2, flex.chi1, flex.chi2)
        ans = cross.cross_point(x_T, H1, H2)
        if ans:
            file.write(f'{flex.N2}   {flex.sigma1}   {ans[0]}   {ans[1]} \n') 
        else:
            file.write(f'{flex.N2}   {flex.sigma1}   -   - \n')
        print_fig(f'N2={flex.N2}, sigma={flex.sigma2}.jpg', x_T, H1, H2)