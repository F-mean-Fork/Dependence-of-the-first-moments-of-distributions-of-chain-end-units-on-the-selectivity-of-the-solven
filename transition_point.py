from flex_api import *
import operator
from scipy import interpolate

def run_on_chi(Point, chi2, timeout = 300):
	Point.chi2 = chi2
	Flex_api.clear()
	Point.print_input()
	if Point.run_flex(timeout):
		Point.read_data()
		return Point.H1, Point.H2
	else:
		return None

if __name__ == '__main__':
    EPS = 1e-4
    DELTA = 0.2
    TIMEOUT = 600
    Point = Flex_api(100, 0.02, 1.0, 0.0, 120, 0.02, 1.0, 0.0)
    if not os.path.isfile('flex.exe'):
        Flex_api.load_flex()
    # os._exit(0)
    for p in np.arange(1.0, 10.1, 0.5):
        Point.p2 = p
        Point.print_input()
        Point.run_flex(timeout=300)
        Point.read_data()
        Point.profiles()
        chi, H1, H2 = list(), list(), list() 
        delta = DELTA
        chi.append(-delta)
        while delta > EPS:
            chi[-1] += delta
            Flex_api.clear()
            Flex_api.clear_initial_guess()
            calc = run_on_chi(Point, chi[-1], timeout = TIMEOUT)
            if calc:
                t1, t2 = calc
                H1.append(t1)
                H2.append(t2)
                print(chi[-1], H1[-1], H2[-1])
                if H2[-1] <= H1[-1]:
                    chi.append(chi[-1] - delta)
                    delta = 0.5 * delta
                else:
                    chi.append(chi[-1])
            else:
                break
        chi.pop(-1)
        chi0 = chi[-1]
        H0 = (H1[-1]+H2[-1])*0.5
        L = sorted(zip(chi,H1,H2), key=operator.itemgetter(0))
        chi, H1, H2 = zip(*L)
        with open('first_moments.txt', 'w') as file:
            for x, y, z in zip(chi, H1, H2):
                file.write(f'{x} {y} {z} \n')
        if delta <= EPS:
            diff_H = [(i - j)/H0 for i, j in zip(H1, H2)]
            diff_H = np.gradient(diff_H)/np.gradient(chi)
            dHdT = diff_H[chi.index(chi0)]
            #dHdT = interpolate.InterpolatedUnivariateSpline(chi, diff_H)(H0)
            delta_T = 1.0 / dHdT
        else:
            chi0 = None
            H0 = None
            delta_T = None
        with open('data_result.txt', 'a+') as file:
            file.write(f'{Point.sigma2} {Point.p2} {chi0} {H0} {delta_T} \n')
        # Point.profiles(f'sigma2={Point.sigma2}, p2={Point.p2}, chi0={chi0}, phi.jpg')
        # Point.profiles(f'sigma2={Point.sigma2}, p2={Point.p2}, chi0={chi0}, n.jpg')
        # plt.plot(chi, H1, '-o', color = 'b')
        # plt.plot(chi, H2, '-o', color = 'r')
        # plt.show()
        