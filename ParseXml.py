#!/usr/bin/python

import re
import sys

class ParseXml:

	def __init__(self, filename):
		self.dic_t = {}
		self.dic_nt = {}
		self.dic_nts = {}
		self.__buildDics__(filename)
		self.buidStructure = True

	def __buildDics__(self, filename):
		filename = filename
		try:
			xmlfile = open(filename, "r")
		except IOError:
			print 'ERROR: System cannot open the '+filename+' file'
			sys.exit()

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

				self.dic_t[id_t] = {'word':word, 'lemma':lemma, 'pos':pos, 'morph':morph, 'sem':sem, 'extra':extra, 'headof':''}
				
			elif '<nt ' in line:
				id_nt = re.search('(?<=id=")\w+', line).group(0)
				id_nt_number = int(re.search('(?<=_)\w+', line).group(0))
				cat = re.search('(?<=cat=")\w+', line).group(0)
				array_edges = []
				self.dic_nt[id_nt] = {'cat':cat, 'edge':array_edges}
				
			
			elif '<edge ' in line:
				idref = re.search('(?<=idref=")\w+', line).group(0)
				idref_number = int(re.search('(?<=_)\w+', line).group(0))
				label = re.search('(?<=label=")\w+', line).group(0)

				if idref_number < 500 or idref_number > id_nt_number:
					array_edges.append([idref, label])

				if 'H' in label:
					self.dic_t[idref]['headof'] = id_nt
					self.dic_nt[id_nt]['head'] = idref

			elif '</nt>' in line:
				self.dic_nt[id_nt]['edge'] = array_edges	
				
		xmlfile.close()

	def __buildNonTerminalStructure__(self):
		for id_nt in self.dic_nt:
			list_np = []
			for idref in self.dic_nt[id_nt]['edge']:
				list_np.append(idref[0])
			
			inner_count = 0
			while inner_count < len(list_np):
				idref = list_np[inner_count]
				idref_number = int(list_np[inner_count].split('_')[1])
				
				if idref_number > 500:
					list_np.pop(inner_count)
					temp_count = inner_count
					for idref_inner in self.dic_nt[idref]['edge']:
						list_np.insert(temp_count, idref_inner[0])
						temp_count = temp_count + 1					
					inner_count = inner_count - 1
				inner_count = inner_count + 1

			self.dic_nts[id_nt] = {'structure': list_np}

		for id_nts in self.dic_nts:
			phrase = ''
			for id_t in self.dic_nts[id_nts]['structure']:
				phrase += self.dic_t[id_t]['lemma']+' '
			self.dic_nts[id_nts]['phrase'] = phrase.rstrip()

	def getDicTerms(self):
		return self.dic_t

	def getTermsById(self, id_t):
		try:
			term = self.dic_t[id_t]
		except:
			print 'ERROR: Term with ID '+id_t+' was not found'
			sys.exit()
		return term

	def getDicNonTerminals(self):
		return self.dic_nt

	def getNonTerminalsById(self, id_nt):
		try:
			nonterminal = self.dic_nt[id_nt]
		except:
			print 'ERROR: Non terminal with ID '+id_nt+' was not found'
			sys.exit()
		return nonterminal

	def getDicNTStructure(self):
		if self.buidStructure:
			self.__buildNonTerminalStructure__()
			self.buidStructure = False
		return self.dic_nts

	def getNTStructureById(self, id_nts):
		if self.buidStructure:
			self.__buildNonTerminalStructure__()
			self.buidStructure = False
		try:
			nts = self.dic_nts[id_nts]
		except:
			print 'ERROR: Non terminal structure with ID '+id_nts+' was not found'
			sys.exit()
		return nts
	
	def printDicTerms(self):
		for id_t in self.dic_t:
			print 'Key: '+id_t
			print self.dic_t[id_t]
			print '\n'

	def printTermsById(self, id_t):
		try:
			term = self.dic_t[id_t]
		except:
			print 'ERROR: Term with ID '+id_t+' was not found'
			sys.exit()
		print term

	def printDicNonTerminals(self):
		for id_nt in self.dic_nt:
			print 'Key: '+id_nt
			print self.dic_nt[id_nt]

	def printNonTerminalsById(self, id_nt):
		try:
			nonterminal = self.dic_nt[id_nt]
		except:
			print 'ERROR: Non terminal with ID '+id_nt+' was not found'
			sys.exit()
		print nonterminal

	def printDicNTStructure(self):
		if self.buidStructure:
			self.__buildNonTerminalStructure__()
			self.buidStructure = False
		for id_nts in self.dic_nts:
			print 'Key: '+id_nts
			print self.dic_nts[id_nts]

	def printNTStructureById (self, id_nts):
		if self.buidStructure:
			self.__buildNonTerminalStructure__()
			self.buidStructure = False
		try:
			nts = self.dic_nts[id_nts]
		except:
			print 'ERROR: Non terminal structure with ID '+id_nts+' was not found'
			sys.exit()
		print nts
