#!/usr/bin/python

import re

class ParseXml:

	def __init__(self, filename):		
		self.filename = filename
		self.hash_t = {}
		self.hash_nt = {}
		self.buildHashs(filename)

	def buildHashs(self, filename):
		self.filename = filename
		xmlfile = open(filename, "r")

		for line in xmlfile:
			if '<t ' in line:
				id_t = re.search('(?<=id=")\w+', line).group(0)
				word = re.search('(?<=word=")\S+', line).group(0)[0:-1].lower()
				lemma = re.search('(?<=lemma=")\S+', line).group(0)[0:-1].lower()
				morph = re.search('(?<=morph=")[\w -]+', line).group(0)
				sem = re.search('(?<=sem=")[\w -]+', line).group(0)
				extra = re.search('(?<=extra=")[\w -]+', line).group(0)
				
				if re.search('%|&amp;', lemma):
					pos = '--' 
				else:
					pos = re.search('(?<=pos=")\S+', line).group(0)[0:-1]

				self.hash_t[id_t] = {'word':word, 'lemma':lemma, 'pos':pos, 'morph':morph, 'sem':sem, 'extra':extra, 'headof':''}
				
			elif '<nt ' in line:
				id_nt = re.search('(?<=id=")\w+', line).group(0)
				cat = re.search('(?<=cat=")\w+', line).group(0)

				self.hash_nt[id_nt] = {'cat':cat, 'edge':{}}
			
			elif '<edge ' in line:
				label = re.search('(?<=label=")\w+', line).group(0)
				idref = re.search('(?<=idref=")\w+', line).group(0)
				
				self.hash_nt[id_nt]['edge'][idref] = label

				if 'H' in label:
					self.hash_t[idref]['headof'] = id_nt
					self.hash_nt[id_nt]['head'] = idref
					
			elif '</nt>' in line:
				print id_nt
				print self.hash_nt[id_nt]
				print '\n'
		xmlfile.close();
