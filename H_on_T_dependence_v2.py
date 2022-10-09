import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import Cross_point_ver2 as cross
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

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
Temp_value = np.array([280.0, 282.5, 287.5, 292.5, 295.0, 297.5, 307.5, 312.5, 320.0, 322.5])
Temp_value = Temp_value[:, np.newaxis]
chi1_T = np.array([1.44, 1.29, 1.0, 0.75, 0.63, 0.5, 0.13, -0.03, -0.188, -0.226])
chi1_T = chi1_T[:, np.newaxis]
chi2_T = np.array([-0.6, -0.5, -0.3, -0.102, 0.0, 0.108, 0.5, 0.688, 0.983, 1.08])
chi2_T = chi2_T[:, np.newaxis]
T_0 = 280.0; T_max = 330.0; delta_T = 0.5
Temperature = np.arange(T_0, T_max, delta_T)
Temperature = Temperature[:, np.newaxis]
DEGREE = 3
model = make_pipeline(PolynomialFeatures(DEGREE), Ridge())
model.fit(Temp_value, chi1_T)
chi1_T = model.predict(Temperature)
model.fit(Temp_value, chi2_T)
chi2_T = model.predict(Temperature)

flex = Flex_api(100, 0.01, 1.0, 0.0, 100, 0.01, 1.0, 0.25)  #Here we enter values to run Flex_api class. N2 can be any, cause we create a cycle for it
flex.swpro = 0
with open("Data_result.txt", "a") as file:
    for n in range(100, 201, 5):                            #Enter range of N2 values
        flex.N2 = n
        H1 = []
        H2 = []
        x_T = []
        for chi1, chi2, T in zip(chi1_T, chi2_T, Temperature):                                        #Cycle for Chi parameter changing
            flex.chi2 = chi2[0]
            flex.chi1 = chi1[0]
            flex.print_input()
            if os.name == 'nt':
                os.system(r'.\flex.exe')
            else:
                os.system(r'./flex.exe')
            t1, t2 = flex.read_data()
            H1.append(t1)
            H2.append(t2)
            x_T.append(T[0])
            print(T[0], t1, t2, flex.chi1, flex.chi2)    
        ans = cross.cross_point(x_T, H1, H2)
        diff_H = [(i - j)/ans[1] for i, j in zip(H1, H2)]
        diff_H = np.gradient(diff_H)/np.gradient(x_T)
        dHdT = interpolate.InterpolatedUnivariateSpline(x_T, diff_H)(ans[0])
        #plt.plot(x_T, diff_H)
        #plt.plot(ans[0],dHdT), 'o')
        #plt.show()
        #plt.close()
        if ans:
            file.write(f'{flex.N2}   {flex.sigma1}   {ans[0]}   {ans[1]}   {dHdT}\n')
        else:
            file.write(f'{flex.N2}   {flex.sigma1}   -   -   - \n')
        print_fig(f'H_T_N2={flex.N2}_sigma={flex.sigma2}.jpg', x_T, H1, H2)
   