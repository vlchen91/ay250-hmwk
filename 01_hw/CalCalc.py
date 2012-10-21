'''
CalCalc.py
Author: Victor Chen
Description: The CalCalc module contains one function: calculate. It's just used for
evaluating a mathematical expression, and if that fails, it will ask Wolfram Alpha
for an answer.
'''

from math import *
import urllib2 as ul2
from xml.dom.minidom import parseString # should be in every standard Python
import argparse

def calculate(question):
	'''Calculate an answer to a question. Will perform an "eval()" or fetch from W|A.

	Keyword argument:
	question -- a string of the expression'''	
	
	def calculate_offline():
		'''Calculate the answer to a mathematical expression.'''
		answer = eval(question)
		return answer
	
	def calculate_online():
		'''Fetch an answer from Wolfram|Alpha.'''
		file = ul2.urlopen('http://api.wolframalpha.com/v2/query?input=' +\
	 					   '%20'.join(question.split()) +\
	 					   '&appid=UAGAWR-3X6Y8W777Q')
		data = file.read()
		file.close()
		dom = parseString(data)
		xmlTag = dom.getElementsByTagName('pod')
		dom2 = parseString(xmlTag[1].toxml())
		xmlTag2 = dom2.getElementsByTagName('plaintext')
		result = xmlTag2[0].toxml().replace('<plaintext>','').replace('</plaintext>','')
		return result
	
	
	try:
		return calculate_offline()
	except:
		return calculate_online()
		
		
# Parse command-line arguments		
parser = argparse.ArgumentParser(description='Python Calculator/W|A Fetcher')
parser.add_argument(nargs='*', dest='query', default=[],
					help='(Optional) Ask a question on Cmd Line/Terminal')
args_lst = parser.parse_args()

if __name__ == '__main__':
	if not (args_lst.query == []):
		calculate(' '.join(args_lst.query))
		
# Nosetests
def test_1():
	# test if eval works in calculate
	assert calculate('5+5+5+5+5+5') == 30
	
def test_2():
	# test if argparse parses expressions correctly
	assert calculate('5 + 5 + 5 + 5 + 5 + 5') == 30

def test_3():
	# test if math module works with calculate
	assert calculate('sin(pi / 2.)') == 1.

def test_4():
	# test if Wolfram|Alpha works
	assert calculate('Distance from New York to San Francisco') == u'2577 miles'
	
def test_5():
	# test if Wolfram|Alpha works
	assert calculate('Meaning to life') == u'42\n(according to Douglas Adams\'' +\
					 ' humorous science-fiction novel The Hitchhiker\'s Guide' +\
					 ' to the Galaxy)'