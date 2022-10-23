import matplotlib.pyplot as plt
import numpy as np

# def print_fig():
#     with open('sigma_0.01_p1=p2.txt', 'r') as f:
#         data_1 = []
#         for line in f.readlines():
#             data_1.append(list(map(float, line.split())))
#         data_1 = np.array(data_1)
#         x = data_1[:, 1] 
#         y1 = data_1[:, 2]
#         intervals1 = data_1[:, 4] / 2 
#     with open('sigma_0.02_p1=p2.txt', 'r') as d:
#         data_2= []
#         for line in d.readlines():
#             data_2.append(list(map(float, line.split())))
#         data_2 = np.array(data_2)
#         y2 = data_2[:, 2]
#         intervals2 = data_2[:, 4] / 2 
#     with open('sigma_0.1_p1=p2.txt', 'r') as e:
#         data_3 = []
#         for line in e.readlines():
#             data_3.append(list(map(float, line.split())))
#         data_3 = np.array(data_3)
#         y3 = data_3[:, 2] 
#         intervals3 = data_3[:, 4] / 2
    
def print_fig():
    with open('sigma_0.01_p2.txt', 'r') as f:
        data_1 = []
        for line in f.readlines():
            data_1.append(list(map(float, line.split())))
        data_1 = np.array(data_1)
        x = data_1[:, 1] 
        y1 = data_1[:, 2]
        intervals1 = data_1[:, 4] / 2 
    # with open('sigma_0.02_p2.txt', 'r') as d:
    #     data_2= []
    #     for line in d.readlines():
    #         data_2.append(list(map(float, line.split())))
    #     data_2 = np.array(data_2)
    #     y2 = data_2[:, 2]
    #     intervals2 = data_2[:, 4] / 2 
    with open('sigma_0.1_p2.txt', 'r') as e:
        data_3 = []
        for line in e.readlines():
            data_3.append(list(map(float, line.split())))
        data_3 = np.array(data_3)
        y3 = data_3[:, 2] 
        intervals3 = data_3[:, 4] / 2
        
    plt.errorbar(x, y1, color = 'black', label = r'$\sigma$ = 0.01', linewidth= 1,
    yerr=intervals1, marker='o', markersize = 4, ecolor='red', elinewidth=1, capsize=12, capthick=0.8)
    # plt.errorbar(x, y2, color = 'blue', label = r'$\sigma$ = 0.01', linewidth= 1,
    # yerr=intervals1, marker='o', markersize = 4, ecolor='violet', elinewidth=1, capsize=12, capthick=0.8)
    plt.errorbar(x, y3, color = 'green', label = r'$\sigma$ = 0.01', linewidth= 1.5,
    yerr=intervals3, marker='o', markersize = 4, ecolor='darkorange', elinewidth=1.5, capsize=12, capthick=0.8)
    plt.xlabel('P')
    plt.ylabel(r'$\chi$')
    plt.grid()  
    plt.legend(fontsize=10)
    plt.draw()
    # plt.savefig('p1=p2.jpg', dpi=300)
    plt.savefig('p2.jpg', dpi=300)
    plt.close()

print_fig()