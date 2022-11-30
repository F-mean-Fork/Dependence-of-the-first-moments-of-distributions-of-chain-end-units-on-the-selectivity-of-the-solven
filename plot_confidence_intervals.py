import matplotlib.pyplot as plt
import numpy as np

#read data from files#

# def print_fig():
#     with open('sigma_0.01_p2.txt', 'r') as f:
#         data_1 = []
#         for line in f.readlines():
#             data_1.append(list(map(float, line.split())))
#         data_1 = np.array(data_1)
#         x = data_1[:, 0] 
#         y1 = data_1[:, 1]
#         # intervals1 = data_1[:, 3] / 2 
#     with open('sigma_0.06_p2.txt', 'r') as d:
#         data_2= []
#         for line in d.readlines():
#             data_2.append(list(map(float, line.split())))
#         data_2 = np.array(data_2)
#         x1 = data_2[:, 0]
#         y2 = data_2[:, 1]
#         # intervals2 = data_2[:, 3] / 2 
#     with open('sigma_0.1_p2.txt', 'r') as e:
#         data_3 = []
#         for line in e.readlines():
#             data_3.append(list(map(float, line.split())))
#         data_3 = np.array(data_3)
#         y3 = data_3[:, 1] 
#         # intervals3 = data_3[:, 3] / 2
#     with open('sigma_0.03_p2.txt', 'r') as g:
#         data_4= []
#         for line in g.readlines():
#             data_4.append(list(map(float, line.split())))
#         data_4 = np.array(data_4)
#         y4 = data_4[:, 1]
    
def print_fig():
    with open('sigma_0.01_p2.txt', 'r') as f:
        data_1 = []
        for line in f.readlines():
            data_1.append(list(map(float, line.split())))
        data_1 = np.array(data_1)
        x = data_1[:, 0] 
        y1 = data_1[:, 1] 
    with open('sigma_0.03_p2.txt', 'r') as d:
        data_2= []
        for line in d.readlines():
            data_2.append(list(map(float, line.split())))
        data_2 = np.array(data_2)
        y2 = data_2[:, 1]
    with open('sigma_0.06_p2.txt', 'r') as e:
        data_3 = []
        for line in e.readlines():
            data_3.append(list(map(float, line.split())))
        data_3 = np.array(data_3)
        x1 = data_3 [:, 0]
        y3 = data_3[:, 1] 
    with open('sigma_0.1_p2.txt', 'r') as g:
        data_4= []
        for line in g.readlines():
            data_4.append(list(map(float, line.split())))
        data_4 = np.array(data_4)
        y4 = data_4[:, 1]
        
    # Plot a errorbar graph #
    
    # plt.errorbar(x, y1, color = 'black', label = r'$\sigma$ = 0.01', linewidth= 1,
    # yerr=intervals1, marker='o', markersize = 4, ecolor='red', elinewidth=1, capsize=8, capthick=0.8)
    # plt.errorbar(x, y2, color = 'blue', label = r'$\sigma$ = 0.03', linewidth= 1,
    # yerr=intervals2, marker='o', markersize = 4, ecolor='steelblue', elinewidth=1, capsize=4, capthick=0.8)
    # # plt.plot(x, y2, '--o', label = r'$\sigma$ = 0.03', linewidth= 1)
    # plt.errorbar(x, y3, color = 'green', label = r'$\sigma$ = 0.1', linewidth= 1.5,
    # yerr=intervals3, marker='o', markersize = 4, ecolor='violet', elinewidth=1.5, capsize=4, capthick=0.8)

    # Plot a chi on p/a dependence graph #
    
    plt.plot(x, y4, color = 'green', label = r'$\sigma$ = 0.1', linewidth= 1.5)
    plt.plot(x1, y3, color = 'red', label = r'$\sigma$ = 0.06', linewidth= 1.5)
    plt.plot(x, y2, color = 'violet', label = r'$\sigma$ = 0.03', linewidth= 1.5)
    plt.plot(x, y1, color = 'blue', label = r'$\sigma$ = 0.01', linewidth= 1.5)
    
    plt.xlabel('$p/a$', size=18)
    plt.ylabel(r'$\chi*$', size=18)
    plt.grid()  
    plt.xlim(1., 7.)
    plt.ylim(0., 2.5)
    plt.legend(fontsize=16)
    plt.draw()
    plt.show()
    # plt.savefig('p1=p2.jpg', dpi=300)
    # plt.savefig('p2_0.01_0.02_0.1.jpg', dpi=300)
    # plt.close()

print_fig()