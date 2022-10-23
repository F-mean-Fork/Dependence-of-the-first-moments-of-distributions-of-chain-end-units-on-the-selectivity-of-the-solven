import os
import shutil
import numpy as np
import subprocess
import matplotlib.pyplot as plt
import operator

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
		self.H1 = None                      #first moment of chain A
		self.H2 = None                      #first moment of chain B      
		self.F = None                       #free energy of the system
        
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
   
	@staticmethod
	def check_infor():
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
				self.H1 = st[0]
				self.H2 = st[1]
				self.F = st[2]
		except:
			self.H1 = None                     
			self.H2 = None                       
			self.F = None 

	@staticmethod
	def run_flex(timeout):
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
	
	@staticmethod
	def load_flex():
		if os.name == 'nt':
			dir_name = r'Flex_2_2\Source'
			path = r'Flex_2_2\flex.exe'
		else:
			dir_name = 'Flex_2_2/Source'
			path = 'Flex_2_2/flex.exe'
		try:
			shutil.rmtree('Flex_2_2')
		except:
			pass
		os.system('git clone https://github.com/IvanMikhailovIMCRAS/Flex_2_2.git')
		os.chdir(dir_name) 
		os.system('make')
		os.chdir('..')
		os.chdir('..')
		shutil.copy(path,'flex.exe')

	@staticmethod
	def clear():
		for file in ['data.out', 'INFOR.info','INPUT.txt', 'profiles.out']:
			try:
				os.remove(file)
			except:
				pass
						
	@staticmethod
	def clear_initial_guess():
		try:
			os.remove('initial_guess.in')
		except:
			pass

	def profiles(self):
		try:
			with open('profiles.out', 'r') as f:
				f.readline()
				profile = []
				for line in f.readlines():
					profile.append(list(map(float, line.split())))
			profile = np.array(profile)
			z = profile[:, 0]; phi1 = profile[:, 1]; phi2 = profile[:, 2]; n1 = profile[:, 3]; n2 = profile[:, 4] 
			x_lim = max(self.H1, self.H2) * 2
			y_lim = max(max(phi1), max(phi2)) * 1.05
			plt.xlim(0., x_lim)
			plt.ylim(0., y_lim)
			plt.xlabel(r'$z$', size=16)
			plt.ylabel(r'$\varphi(z)$', size=16)
			plt.plot(z, phi1, color='black', label='Chain A')
			plt.plot(z, phi2, color='red', label='Chain B')
			plt.legend()
			plt.savefig(f'phi, sigma2={self.sigma2}, p2={self.p2}.jpg', dpi=300)
			plt.close()
			y_lim = max(max(n1), max(n2)) * 1.05
			plt.xlim(0., x_lim)
			plt.ylim(0., y_lim)
			plt.xlabel(r'$z$', size=16)
			plt.ylabel(r'$n(z)$', size=16)
			plt.plot(z, n1, color='black', label='Chain A')
			plt.plot(z, n2, color='red', label='Chain B')
			plt.legend()
			plt.savefig(f'n, sigma2={self.sigma2}, p2={self.p2}.jpg', dpi=300)
			plt.close()
		except IOError as err:
			print(err)