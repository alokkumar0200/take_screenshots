#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import sys
import os, time


dirs = []
report = ''
html = ''
domain = ''
output = ''
folder_for_results = '/home/devil/Documents/results/'				#Change this path to results directory
selenium_driver = '/home/devil/take_screenshots/geckodriver'				#Change this to path of selenium driver (geckodriver for firefox | chromedriver for chrome)
TEMPLATE_FILE = '/home/devil/take_screenshots/template'

def check_args():
	global dirs, folder_for_results
	global domain
	global output
	try:
		if len(sys.argv) == 4:
			if os.path.exists(sys.argv[1]):
				file_path = sys.argv[1]
				domain = sys.argv[2].strip('/')
				output = sys.argv[3]
				###
				folder_for_results += output
				os.makedirs(folder_for_results)
				###
				with open(file_path) as file:
					dirs = file.readlines()
				return dirs, domain
			else:
				raise Exception()
		else:
			raise Exception()
	
	except (Exception) as error:
		print('Error: Invalid Arguments Supplied\nUsage: python take_screenshots.py path/to/file http://www.example.com output_file_name')
		sys.exit()

def write_file(location, file_name, data):
	file = '/'+location.strip('/') + '/' + file_name + '.html'
	f = open(file, 'w')
	f.write('<html><body>'+data+'</body></html>')
	f.close()

def gen_report(path, domain):
	global report
	text = ''

	with open(TEMPLATE_FILE) as file:
		text = file.read()
		text = text.replace('PATH', path)
		text = text.replace('DOMAIN', domain)

	report += str(text)


def main():
	global report
	args= check_args()
	try:
		if os.path.exists(selenium_driver):
			options = Options()
			options.add_argument('--headless')
			browser = webdriver.Firefox(options=options, executable_path=selenium_driver)			#Comment this line if using chrome instead of firefox
			# browser = webdriver.Chrome(options=options, executable_path=selenium_driver)			#And uncomment this line for Chrome
			for x in dirs:
				image = x.split(' ')[0].strip('/')[:-1]+'.png'
				addr = domain+'/'+x.split(' ')[0].strip('/')
				print('[*] Domain: %s' %(addr))
				browser.get(addr)
				browser.save_screenshot(folder_for_results + '/'+image)
				gen_report(image, addr)
			write_file(folder_for_results, output,report)
			browser.quit()
			print("Results are saved to {}".format(folder_for_results))
		else:
			raise Exception()
	except Exception as error:
		print(error)
		sys.exit()


if __name__ == '__main__':
	main()