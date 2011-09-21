#!/usr/bin/python

import sys
import re
import codecs

class Parameters:
	def __init__(self):		
		self.dic_parameters = {}
		self.__buildDic__()

	def __buildDic__(self):
		try:
			file_parameters = codecs.open('parameters.cfg', 'r', 'utf-8')
		except IOError:
			print 'ERROR: System cannot open the parameters.cfg file'
			sys.exit()

		for line in file_parameters:
			if re.match('max_qty_terms', line):
				self.dic_parameters['max_qty_terms'] = line.split('=')[1].replace('\n','')
			if re.match('min_freq_t3', line):
				self.dic_parameters['min_freq_t3'] = line.split('=')[1].replace('\n','')
			if re.match('min_word_size', line):
				self.dic_parameters['min_word_size'] = line.split('=')[1].replace('\n','')
			if re.match('svd_treshold', line):
				self.dic_parameters['svd_treshold'] = line.split('=')[1].replace('\n','')
			if re.match('min_freq_t2', line):
				self.dic_parameters['min_freq_t2'] = line.split('=')[1].replace('\n','')
			if re.match('mi_precision', line):
				self.dic_parameters['mi_precision'] = line.split('=')[1].replace('\n','')
			if re.match('window_size', line):
				self.dic_parameters['window_size'] = line.split('=')[1].replace('\n','')

		file_parameters.close()

	def getMaxQtyTerms(self):
		return int(self.dic_parameters['max_qty_terms'])

	def getMinFreqT3(self):
		return int(self.dic_parameters['min_freq_t3'])

	def getMinWordSize(self):
		return int(self.dic_parameters['min_word_size'])

	def getSVDThreshold(self):
		return int(self.dic_parameters['svd_treshold'])

	def getMinFreqT2(self):
		return int(self.dic_parameters['min_freq_t2'])

	def getMIPrecision(self):
		return int(self.dic_parameters['mi_precision'])

	def getWindowSize(self):
		return int(self.dic_parameters['window_size'])

	def getDicParameters(self):
		return self.dic_parameters

	def printDicParameters(self):
		print self.dic_parameters

	def setMaxQtyTerms(self, qtd_terms):
		self.dic_parameters['max_qty_terms'] = qtd_terms

	def setMinFreqT3(self, freq):
		self.dic_parameters['min_freq_t3'] = freq

	def setMinWordSize(self, size):
		self.dic_parameters['min_word_size'] = size

	def setSVDThreshold(self, threshold):
		self.dic_parameters['svd_treshold'] = threshold

	def setMinFreqT2(self, freq):
		self.dic_parameters['min_freq_t2'] = freq

	def setMIPrecision(self, precision):
		self.dic_parameters['mi_precision'] = precision

	def setWindowSize(self, window_size):
		self.dic_parameters['window_size'] = window_size

