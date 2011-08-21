#!/usr/bin/python

import re

class ParseCg:

	def __init__(self, filename):		
		self.filename = filename
		self.hash_t = {}
		self.__buildHash__(filename)

	def __buildHash__(self, filename):
		self.filename = filename
		cgfile = open(filename, "r")
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
				self.hash_t[id_t] = {'word':word, 'lemma':lemma, 'synt':synt, 'extra':extra}
			elif '$' in line:
				word = line[1]
				self.hash_t[id_t] = {'word':word, 'lemma':'--', 'synt':'--', 'extra':'--'}
			elif '</s>' in line:
				sentence = sentence + 1
				count_line = 0
			count_line = count_line + 1

	def getHashTerms(self):
		return self.hash_t

	def printHashTerms(self):
		for id_t in self.hash_t:
			print 'Key: '+id_t
			print self.hash_t[id_t]
