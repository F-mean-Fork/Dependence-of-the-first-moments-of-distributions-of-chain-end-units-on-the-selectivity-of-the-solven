from decimal import DivisionByZero
from more_itertools import divide
from flex_api import *
import operator
from scipy import interpolate
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from scipy import interpolate
from scipy.interpolate import UnivariateSpline

def deviation(x, x0, y):
    x = np.array(x)
    y = np.array(y)
    norm = 0.0 
    norm_2 = 0.0
    for i in range(len(x-1)):
        if x[i] > x0:
            break
        s = (x[i+1]-x[i])*(y[i+1]+y[i])*0.5 
        norm += s 
        norm_2 += (x[i+1]-x[i])*(y[i+1]*(x[i+1]-x0)**2+y[i]*(x[i]-x0)**2)*0.5 
    return np.sqrt(norm_2/norm)  

def deviation_2(x, x0, y):
    x = np.array(x)
    y = np.array(y)
    norm = 0.0 
    for i in range(len(x-1)):
        if x[i] > x0:
            break
        s = (x[i+1]-x[i])*(y[i+1]+y[i])*0.5 
        norm += s 
    y = y / norm
    y_0 = np.max(y)
    return 1/(np.sqrt(2*np.pi)*y_0)

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
    DELTA = 0.01
    TIMEOUT = 80
    MAXVALUE = 1.0e6
    Point = Flex_api(200, 0.1, 1.0, 0.0, 240, 0.1, 1.0, 0.0)
    
    if not os.path.isfile('flex.exe'):
        Flex_api.load_flex()  
    for p in np.arange(4.5, 7.1, 0.5):
        Point.p2 = p
        # Point.p1 = p
        Point.print_input()
        Flex_api.clear()
        Flex_api.clear_initial_guess()
        Point.run_flex(timeout=TIMEOUT)
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
            diff_H = - np.gradient(H2)/np.gradient(chi)
            diff_H = [i - diff_H[0] if i > diff_H[0] else 0.0 for i in diff_H]
            delta_chi = deviation_2(chi, chi0, diff_H)
        else:
            chi0 = chi[-1]
            H0 = (H1[-1]+H2[-1])*0.5
            delta_chi = 0.0
        with open('data_result.txt', 'a+') as file:
            file.write(f'{Point.p2} {chi0} {H0} {delta_chi} \n')
        # plt.plot(chi, H1, color = 'black')
        # plt.plot(chi, H2, color = 'red')
        # plt.show()