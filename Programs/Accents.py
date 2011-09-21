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
				code = line.split('=')[1].replace('\n','')
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

	def buildCodes(self, raw_lemma):
		for cod in self.dic_accents:
			if cod in raw_lemma:
				raw_lemma = raw_lemma.replace(cod, self.dic_accents[cod])
		return raw_lemma

	def buildAccents(self, coded_lemma):
		for cod in self.dic_accents:
			if self.dic_accents[cod] in coded_lemma:
				coded_lemma = coded_lemma.replace(self.dic_accents[cod], cod)
		return coded_lemma
