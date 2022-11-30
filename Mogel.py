import matplotlib.pyplot as plt
import numpy as np

def print_fig():
    with open('p1=1_p2=1_N1=100_N2=120.txt', 'r') as a:
        data_1 = []
        for line in a.readlines():
            data_1.append(list(map(float, line.split())))
        data_1 = np.array(data_1)
        x1 = data_1[:, 2] 
        y1 = data_1[:, 3] 
    with open('p1=1_p2=1_N1=200_N2=240.txt', 'r') as b:
        data_2 = []
        for line in b.readlines():
            data_2.append(list(map(float, line.split())))
        data_2 = np.array(data_2)
        x2 = data_2[:, 2] 
        y2 = data_2[:, 3] 
    with open('p1=1_p2=2_N1=100_N2=120.txt', 'r') as c:
        data_3 = []
        for line in c.readlines():
            data_3.append(list(map(float, line.split())))
        data_3 = np.array(data_3)
        x3 = data_3[:, 2] 
        y3 = data_3[:, 3] 
    with open('p1=1_p2=2_N1=200_N2=240.txt', 'r') as d:
        data_4 = []
        for line in d.readlines():
            data_4.append(list(map(float, line.split())))
        data_4 = np.array(data_4)
        x4 = data_4[:, 2] 
        y4 = data_4[:, 3] 
    with open('p1=1_p2=3_N1=100_N2=120.txt', 'r') as e:
        data_5 = []
        for line in e.readlines():
            data_5.append(list(map(float, line.split())))
        data_5 = np.array(data_5)
        x5 = data_5[:, 2] 
        y5 = data_5[:, 3] 
        
    with open('p1=1_p2=3_N1=200_N2=240.txt', 'r') as f:
        data_6 = []
        for line in f.readlines():
            data_6.append(list(map(float, line.split())))
        data_6 = np.array(data_6)
        x6 = data_6[:, 2] 
        y6 = data_6[:, 3] 
        
    with open('p1=1_p2=4_N1=100_N2=120.txt', 'r') as g:
        data_7 = []
        for line in g.readlines():
            data_7.append(list(map(float, line.split())))
        data_7 = np.array(data_7)
        x7 = data_7[:, 2] 
        y7 = data_7[:, 3] 
        
    with open('p1=1_p2=4_N1=200_N2=240.txt', 'r') as h:
        data_8 = []
        for line in h.readlines():
            data_8.append(list(map(float, line.split())))
        data_8 = np.array(data_8)
        x8 = data_8[:, 2] 
        y8 = data_8[:, 3] 
        
    with open('p1=1_p2=5_N1=100_N2=120.txt', 'r') as j:
        data_9 = []
        for line in j.readlines():
            data_9.append(list(map(float, line.split())))
        data_9 = np.array(data_9)
        x9 = data_9[:, 2] 
        y9 = data_9[:, 3] 
        
    with open('p1=1_p2=5_N1=200_N2=240.txt', 'r') as k:
        data_10 = []
        for line in k.readlines():
            data_10.append(list(map(float, line.split())))
        data_10 = np.array(data_10)
        x10 = data_10[:, 2] 
        y10 = data_10[:, 3] 

    plt.plot(x9, y9, color = 'purple', label = '$p_B = 5$', linewidth= 1.5)
    plt.plot(x10, y10, color = 'purple', linestyle = '--', linewidth= 1.5)
    plt.plot(x7, y7, color = 'violet', label = '$p_B = 4$', linewidth= 1.5)
    plt.plot(x8, y8, color = 'violet', linestyle = '--', linewidth= 1.5)
    plt.plot(x5, y5, color = 'green', label = '$p_B = 3$', linewidth= 1.5)
    plt.plot(x6, y6, color = 'green', linestyle = '--', linewidth= 1.5)
    plt.plot(x3, y3, color = 'red', label = '$p_B = 2$', linewidth= 1.5)
    plt.plot(x4, y4, color = 'red', linestyle = '--', linewidth= 1.5)                    
    plt.plot(x1, y1, color = 'blue', label = '$p_B = 1$', linewidth= 1.5)
    plt.plot(x2, y2, color = 'blue', linestyle = '--', linewidth= 1.5)

    plt.xlabel('$\sigma$', size=18)
    plt.ylabel('$\chi*$', size=18)
    plt.grid()  
    plt.xlim(0.02, 0.08)
    plt.xticks([0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08], [0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04])
    plt.ylim(0., 1.)
    plt.legend(fontsize=12.5, loc = (0.75 ,0.005))
    plt.draw()
    plt.show()
    
print_fig()