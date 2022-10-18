from gettext import npgettext
import os
import shutil
import numpy as np
import subprocess
import matplotlib.pyplot as plt

class Flex_api:
	def __init__(self, N1, sigma1, p1, chi1, N2, sigma2, p2, chi2):
		self.N1 = N1                        #polymerization degree
		self.sigma1 = sigma1                #grafting density
		self.p1 = p1                        #Kuhn length
		self.chi1 = chi1                    #Flory's parameter for polymer-solvent
		self.N2 = N2                        #polymerization degree
		self.sigma2 = sigma2                #grafting density
		self.p2 = p2                        #Kuhn length
		self.chi2 = chi2                    #Flory's parameter for polymer-solvent
		self.chi12 = 0.0                    #Flory's parameter for polymer-polymer
		self.eta = 0.04  
		self.ksi = 0.1                      #step size of gradient descent
		self.nfree = 5000                   #number of "free steps" at descent
		self.swpro = 1                      #if swpro=0: switch off print of profile
        
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
			f.write(f'{self.ksi} \n')
			f.write(f'{self.nfree} \n')
			f.write(f'{self.swpro} \n')
    
	def check_infor(self):
		try:
			path = str(os.system('pwd'))
			if os.name == 'nt':
				path = path+r'\INFOR.info'
			else:
				path = path+r'/INFOR.info'
			with open(path, 'r') as file:
				array = [row.strip() for row in file]
			if 'Awesome! Everything was working as it should!' in array:
				return True
		except:
			return False

	def read_data(self):
		try:
			with open('data.out', 'r') as data:
				data.readline()
				st = list(map(float, data.readline().split()))
				H1 = st[0]
				H2 = st[1]
				F = st[2]
			return H1, H2
		except:
			return None

	def run_flex(self, timeout):
		if os.name == 'nt':
			command = r'.\flex.exe'
		else:
			command = r'./flex.exe'
		try:
			proc = subprocess.run(command, timeout=timeout, check=True, stdout=subprocess.PIPE, encoding='utf-8')
			print(proc.stdout) 
		except:
			return False
		return True
	
	def load_flex(self):                  #For Windows OS
		dir_name = 'Flex_2_2\\Source'
		try:
			shutil.rmtree('Flex_2_2')
		except:
			pass
		os.system('git clone https://github.com/IvanMikhailovIMCRAS/Flex_2_2.git')
		os.chdir(dir_name) 
		os.system('make')
		os.chdir('..')
		os.chdir('..')
		shutil.copy('Flex_2_2\\flex.exe','flex.exe')

	def clear(self):
		for file in ['data.out', 'INFOR.info','INPUT.txt']:
			try:
				os.remove(file)
			except:
				pass

	def clear_initial_guess(self):
		try:
			os.remove('initial_guess.in')
		except:
			pass

def run_on_chi(point, chi2, H1, H2, timeout = 300):
	point.chi2 = chi2
	point.clear()
	point.print_input()
	if point.run_flex(timeout):
		t1, t2 = point.read_data()
		H1.append(t1)
		H2.append(t2)
		return True
	else:
		return False

if __name__ == '__main__':
	EPS = 1e-4
	point = Flex_api(100, 0.05, 1.0, 0.0, 150, 0.05, 1.0, 0.25)
	point.load_flex()
	H1, H2 = list(), list() 
	point.clear_initial_guess()
	chi = [0.0]
	chi2_delta = 0.2
	while chi2_delta > EPS:
		if run_on_chi(point, chi[-1], H1, H2):
			print(H1[-1], H2[-1])
		else:
			break
		if H2[-1] <= H1[-1]:
			chi2_delta = chi2_delta*0.5
			chi.append(chi[-2]+chi2_delta)
		else:
			chi.append(chi[-1]+chi2_delta)
	chi.pop(-1)
	index = sorted(range(len(chi)), key=lambda k: chi[k])
	chi = np.array(chi)
	H1 = np.array(H1)
	H2 = np.array(H2)
	H1 = H1[index]
	H2 = H2[index]
		
	plt.plot(chi, H1, color = 'b')
	plt.plot(chi, H2, color = 'r')
	plt.show()
	