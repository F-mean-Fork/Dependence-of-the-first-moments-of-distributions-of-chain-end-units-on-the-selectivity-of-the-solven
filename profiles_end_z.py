import matplotlib.pyplot as plt
import numpy as np

name_file = '.jpg'
x_limit = 100
y_limit = 0.105

pA=1
pB=5
chi=2.41

with open('profiles.out', 'r') as f:
    f.readline()
    profile = []
    for line in f.readlines():
        profile.append(list(map(float, line.split())))
    profile = np.array(profile)
    z = profile[:, 0]; phi1 = profile[:, 1]; phi2 = profile[:, 2]; n1 = profile[:, 3]; n2 = profile[:, 4]  
    y_lim = max(max(phi1), max(phi2)) * 1.05    
    plt.xlim(0., x_limit)
    plt.ylim(0., y_lim)
    plt.xlabel(r'$z$', size=18)
    plt.ylabel(r'$\varphi(z)$', size=18)
    plt.plot(z, phi1, color='black', label='Chain A')
    plt.plot(z, phi2, color='red', label='Chain B')
    plt.title(f'$p_A={pA}$,   $p_B={pB}$,   $\chi={chi}$', fontsize=16)
    plt.legend(fontsize = 16)
    plt.show()
    # plt.savefig('phi' + name_file, dpi=300)
    # plt.close()
    y_lim = y_limit
    plt.xlim(0., x_limit)
    plt.ylim(0., y_lim)
    plt.xlabel(r'$z$', size=18)
    plt.ylabel(r'$n(z)$', size=18)
    plt.plot(z, n1, color='black', label='Chain A')
    plt.plot(z, n2, color='red', label='Chain B')
    plt.title(f'$p_A={pA}$,   $p_B={pB}$,   $\chi={chi}$', fontsize=16)
    plt.legend(fontsize = 16)
    # plt.savefig('n' + name_file, dpi=300)
    # plt.close()
    plt.show()