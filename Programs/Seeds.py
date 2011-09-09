#!/usr/bin/python

import sys
import codecs

class Seeds:
	def __init__(self):		
		self.dic_seeds = {}
		self.__buildDic__()

	def __buildDic__(self):
		try:
			file_seeds = codecs.open('seeds.txt', 'r', 'utf-8')
		except IOError:
			print 'ERROR: System cannot open the seeds.txt file'
			sys.exit()

		for line in file_seeds:
			if line != '':
				line = line.replace('\n','')
				self.dic_seeds[line] = line

		file_seeds.close()

	def getQtySeeds(self):
		return len(self.dic_seeds)

	def getSeeds(self):
		return self.dic_seeds

	def printSeeds(self):
		print self.dic_seeds

	def printQtySeeds(self):
		print len(self.dic_seeds)

