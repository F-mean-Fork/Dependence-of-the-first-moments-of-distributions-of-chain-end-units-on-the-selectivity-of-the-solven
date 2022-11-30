import numpy as np
import matplotlib.pyplot as plt

name_file = '.jpg'

#Let`s open these files
with open('P1=1.0, P2=1.0, N2=120, sigma=0.01.txt', 'r') as file:
    data = []
    for line in file.readlines():
        data.append(list(map(float, line.split())))
data = np.array(data)
x_ax_1 = data[:, 0]
y_ax_1 = data[:, 1]
y1_ax_1 = data[:, 2]

with open('P1=1.0, P2=5.0, N2=120, sigma=0.01.txt', 'r') as file:
    data2 = []
    for line in file.readlines():
        data2.append(list(map(float, line.split())))
data2 = np.array(data2)
x_ax_2 = data2[:, 0]
y_ax_2 = data2[:, 1]
y1_ax_2 = data2[:, 2]

with open('P1=5.0, P2=5.0, N2=120, sigma=0.01.txt', 'r') as file:
    data3 = []
    for line in file.readlines():
        data3.append(list(map(float, line.split())))
data3 = np.array(data3)
x_ax_3 = data3[:, 0]
y_ax_3 = data3[:, 1]
y1_ax_3 = data3[:, 2]

#H1 on chi graph
plt.plot(x_ax_1, y_ax_1, color = 'blue', linestyle = '--', linewidth= 1)
plt.plot(x_ax_2, y_ax_2, color = 'red', linestyle = '--', linewidth= 1)
plt.plot(x_ax_3, y_ax_3, color = 'green', linestyle = '--', linewidth= 1)    

#H2 on chi graph
plt.plot(x_ax_1, y1_ax_1, color = 'blue', label = r'$p_A = p_B = 1$', linewidth= 1)
plt.plot(x_ax_2, y1_ax_2, color = 'red',  label = r'$p_A = 1, p_B = 5$', linewidth= 1)
plt.plot(x_ax_3, y1_ax_3, color = 'green', label = r'$p_A = p_B = 5$', linewidth= 1)   

plt.xlim(-0.31, 0.3)
plt.ylim(-30, 30)

plt.xlabel(r'$\chi-\chi*$', size=18)
plt.ylabel(r'$H - H* $', size=18)
plt.title (r'$\sigma = 0.01,     N_B = 120$', fontsize=16)
plt.show()
plt.legend(fontsize = 16)
# plt.savefig('Segregation, sigma = 0.01, N= 120' + name_file, dpi=300)
# plt.close()