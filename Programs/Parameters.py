#!/usr/bin/python

import sys
import re

class Parameters:
	def __init__(self):		
		self.dic_parameters = {}
		self.__buildDic__()

	def __buildDic__(self):
		try:
			file_parameters = open('parameters.cfg', 'r')
		except IOError:
			print 'ERROR: System cannot open the parameters.cfg file'
			sys.exit()

		for line in file_parameters:
			if re.match('max_qtd_terms', line):
				self.dic_parameters['max_qtd_terms'] = line.split('=')[1].replace('\n','')
			if re.match('min_freq_t3', line):
				self.dic_parameters['min_freq_t3'] = line.split('=')[1].replace('\n','')
			if re.match('svd_treshold', line):
				self.dic_parameters['svd_treshold'] = line.split('=')[1].replace('\n','')
			if re.match('min_freq_t2', line):
				self.dic_parameters['min_freq_t2'] = line.split('=')[1].replace('\n','')
			if re.match('mi_precision', line):
				self.dic_parameters['mi_precision'] = line.split('=')[1].replace('\n','')
			if re.match('window_size', line):
				self.dic_parameters['window_size'] = line.split('=')[1].replace('\n','')

	def getMaxQtdTerms(self):
		return self.dic_parameters['max_qtd_terms']

	def getMinFreqT3(self):
		return self.dic_parameters['min_freq_t3']

	def getSVDThreshold(self):
		return self.dic_parameters['svd_treshold']

	def getMinFreqT2(self):
		return self.dic_parameters['min_freq_t2']

	def getMIPrecision(self):
		return self.dic_parameters['mi_precision']

	def getWindowSize(self):
		return self.dic_parameters['window_size']

	def printDicParameters(self):
		print self.dic_parameters

	def setMaxQtdTerms(self, qtd_terms):
		self.dic_parameters['max_qtd_terms'] = qtd_terms

	def setMinFreqT3(self, freq):
		self.dic_parameters['min_freq_t3'] = freq

	def setSVDThreshold(self, threshold):
		self.dic_parameters['svd_treshold'] = threshold

	def setMinFreqT2(self, freq):
		self.dic_parameters['min_freq_t2'] = freq

	def setMIPrecision(self, precision):
		self.dic_parameters['mi_precision'] = precision

	def setWindowSize(self, window_size):
		self.dic_parameters['window_size'] = window_size

