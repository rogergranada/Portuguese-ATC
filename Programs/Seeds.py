#!/usr/bin/python

import sys
import re

class Seeds:
	def __init__(self):		
		self.dic_seeds = {}
		self.__buildDic__()

	def __buildDic__(self):
		try:
			file_seeds = open('seeds.txt', 'r')
		except IOError:
			print 'ERROR: System cannot open the seeds.txt file'
			sys.exit()

		for line in file_seeds:
			if line != '':
				line = line.replace('\n','')
				self.dic_seeds[line] = line

	def getQtySeeds(self):
		return len(self.dic_seeds)

	def getSeeds(self):
		return self.dic_seeds

	def printSeeds(self):
		print self.dic_seeds

	def printQtySeeds(self):
		print len(self.dic_seeds)

