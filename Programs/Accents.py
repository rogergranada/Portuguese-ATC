#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import codecs

class Accents:
	def __init__(self):		
		self.dic_accents = {}
		self.__buildDic__()

	def __buildDic__(self):
		try:
			file_accents = codecs.open('accents.txt', 'r', 'utf-8')
		except IOError:
			print 'ERROR: System cannot open the accents.txt file'
			sys.exit()

		for line in file_accents:
			if line != '':
				line = line.replace('\n','')
				character = line.split('=')[0]
				#print character,' => ',
				code = line.split('=')[1].replace('\n','')
				#print code
				self.dic_accents[character] = code

		file_accents.close()

	def getQtyAccents(self):
		return len(self.dic_accents)

	def getAccents(self):
		return self.dic_accents

	def printAccents(self):
		print self.dic_accents

	def printQtyAccents(self):
		print len(self.dic_accents)

