#!/usr/bin/python

import sys
import re
import codecs

from collections import defaultdict

class Statistic:
	def __init__(self, mi_file):		
		self.dic_mi = defaultdict(dict)
		self.dic_terms_mi = {}
		self.__buildDic__(mi_file)

	def __buildDic__(self, mi_file):
		try:
			file_mi = codecs.open(mi_file, 'r', 'utf-8')
		except IOError:
			print 'ERROR: System cannot open the '+mi_file+' file'
			sys.exit()

		line_number = 0
		for line in file_mi:
			if line_number > 3:
				terms = line.split(' ')[0]
				term1_temp = terms.split('<>')[0]
				term2_temp = terms.split('<>')[1]
				term1_type = term1_temp.split('__')[-1]
				term1 = term1_temp.split('__')[0]
				term2_type = term2_temp.split('__')[-1]
				term2 = term2_temp.split('__')[0]
				rank = re.search('(?<= )\w+', line).group(0)
				true_mi = re.search('(?<=  )\d\.\d+', line).group(0)
				frequencies = re.search('(?<= )\w+ \w+ \w+', line).group(0)
				freq_1 = frequencies.split(' ')[0]
				freq_2 = frequencies.split(' ')[1]
				freq_3 = frequencies.split(' ')[2]
				self.dic_mi[term1][term2] = {'type_1':term1_type, 'type_2':term2_type, 'rank':rank, 'true_mi':true_mi, 'freq_1':freq_1, 'freq_2':freq_2, 'freq_3':freq_3}
				self.dic_mi[term2][term1] = {'type_1':term2_type, 'type_2':term1_type, 'rank':rank, 'true_mi':true_mi, 'freq_1':freq_1, 'freq_2':freq_3, 'freq_3':freq_2}
			line_number += 1
		file_mi.close()

	def getDicMI(self):
		return self.dic_mi

	def printDicMI(self):
		print self.dic_mi

	def getDicForTerm(self, term):
		if self.dic_mi.has_key(term):
			return self.dic_mi[term]
		else:
			print 'ERROR: System cannot found the term "'+term+'"'
	
	def printDicForTerm(self, term):
		if self.dic_mi.has_key(term):
			print self.dic_mi[term]
		else:
			print 'ERROR: System cannot found the term "'+term+'"'
			

