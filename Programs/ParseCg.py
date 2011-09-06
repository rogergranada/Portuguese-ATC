#!/usr/bin/python

import re
import sys

class ParseCg:
	def __init__(self, filename):		
		self.dic_t = {}
		self.__buildDic__(filename)

	def __buildDic__(self, filename):
		try:
			cgfile = open(filename, "r")
		except IOError:
			print 'ERROR: System cannot open the '+filename+' file'
			sys.exit()

		sentence = 1
		count_line = 1
		for line in cgfile:
			id_t = 's'+str(sentence)+'_'+str(count_line)
			if '@' in line:
				word = (line.split(' ')[0]).strip('\t').replace('=','_')
				lemma = ((line.split('[')[1]).split(']')[0]).replace('=','_')
				if '> ' in line:
					extra = ((line.split('@')[0]).split('>')[-1]).strip()
				else:
					extra = ((line.split('@')[0]).split(']')[-1]).strip()
				synt = ('@'+line.split('@')[1]).rstrip('\n ')
				self.dic_t[id_t] = {'word':word, 'lemma':lemma, 'synt':synt, 'extra':extra}
			elif '$' in line:
				word = line[1]
				self.dic_t[id_t] = {'word':word, 'lemma':'--', 'synt':'--', 'extra':'--'}
			elif '</s>' in line:
				sentence = sentence + 1
				count_line = 0
			count_line = count_line + 1
		cgfile.close()

	def getDicTerms(self):
		return self.dic_t

	def getTermsById(self, id_t):
		try:
			term = self.dic_t[id_t]
		except:
			print 'ERROR: Term with ID '+id_t+' was not found'
			sys.exit()
		return term

	def printDicTerms(self):
		for id_t in self.dic_t:
			print 'Key: '+id_t
			print self.dic_t[id_t]

	def printTermsById(self, id_t):
		try:
			term = self.dic_t[id_t]
		except:
			print 'ERROR: Term with ID '+id_t+' was not found'
			sys.exit()
		print term
