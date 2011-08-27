#!/usr/bin/python

import re

from ParseXml import ParseXml
from ParseCg import ParseCg

class SyntacticContexts:

	def __init__(self, filename):		
		self.filename_xml = filename+'.xml'
		self.filename_cg = filename+'.cg'
		self.xml = ParseXml(self.filename_xml)
		self.cg = ParseCg(self.filename_cg)
		self.hash_t_xml = self.xml.getHashTerms()
		self.hash_t_cg = {}
		self.hash_nts = {}
		self.hash_an = {}
		self.hash_sv = {}
		
		self.__extractSVRelations__()

	def __extractANRelations__(self):
		for id_t in self.hash_t_xml:
			if self.hash_t_xml[id_t]['pos'] == 'n' or self.hash_t_xml[id_t]['pos'] == 'prop':
				id_sentence = id_t.split("_")[0]
				id_word = id_t.split("_")[1]

				id_1 = id_sentence+'_'+str((int(id_word) + 1))
				id_2 = id_sentence+'_'+str((int(id_word) + 2))
				id_3 = id_sentence+'_'+str((int(id_word) + 3))

				if self.hash_t_xml.has_key(id_3):
					ids = self.hash_t_xml[id_t]['pos']+':'+self.hash_t_xml[id_1]['pos']+':'+self.hash_t_xml[id_2]['pos']+':'+self.hash_t_xml[id_3]['pos']
					if re.match('^(n|prop):prp:(art|num|pron-indef|pron-poss|pu):(n|prop)$', ids) is not None:
						self.__addElementHashAN__('prep_#'+self.hash_t_xml[id_3]['lemma']+'#'+self.hash_t_xml[id_t]['lemma'])
						self.__addElementHashAN__('prep_#'+self.hash_t_xml[id_t]['lemma']+'#'+self.hash_t_xml[id_3]['lemma'])
					if re.match('^(n|prop):adj:adj:adj$', ids) is not None:
						self.__addElementHashAN__('adj_#'+self.hash_t_xml[id_3]['lemma']+'#'+self.hash_t_xml[id_t]['lemma'])

				if self.hash_t_xml.has_key(id_2):
					ids = self.hash_t_xml[id_t]['pos']+':'+self.hash_t_xml[id_1]['pos']+':'+self.hash_t_xml[id_2]['pos']
					if re.match('^(n|prop):prp:(n|prop)$', ids) is not None:
						self.__addElementHashAN__('prep_#'+self.hash_t_xml[id_2]['lemma']+'#'+self.hash_t_xml[id_t]['lemma'])
						self.__addElementHashAN__('prep_#'+self.hash_t_xml[id_t]['lemma']+'#'+self.hash_t_xml[id_2]['lemma'])
					if re.match('^(n|prop):adj:adj$', ids) is not None:
						self.__addElementHashAN__('adj_#'+self.hash_t_xml[id_2]['lemma']+'#'+self.hash_t_xml[id_t]['lemma'])
				
				if self.hash_t_xml.has_key(id_1):
					ids = self.hash_t_xml[id_t]['pos']+':'+self.hash_t_xml[id_1]['pos']
					if re.match('^(n|prop):adj$', ids) is not None:
						self.__addElementHashAN__('adj_#'+self.hash_t_xml[id_1]['lemma']+'#'+self.hash_t_xml[id_t]['lemma'])
					if re.match('^(n|prop):(n|prop)$', ids) is not None:
						self.__addElementHashAN__('nn_#'+self.hash_t_xml[id_1]['lemma']+'#'+self.hash_t_xml[id_t]['lemma'])
						self.__addElementHashAN__('nn_#'+self.hash_t_xml[id_t]['lemma']+'#'+self.hash_t_xml[id_1]['lemma'])

				id_1 = id_sentence+'_'+str((int(id_word) - 1))
				id_2 = id_sentence+'_'+str((int(id_word) - 2))
				id_3 = id_sentence+'_'+str((int(id_word) - 3))

				if self.hash_t_xml.has_key(id_3):
					ids = self.hash_t_xml[id_3]['pos']+':'+self.hash_t_xml[id_2]['pos']+':'+self.hash_t_xml[id_1]['pos']+':'+self.hash_t_xml[id_t]['pos']
					if re.match('^adj:adj:adj:(n|prop)$', ids) is not None:
						self.__addElementHashAN__('adj_#'+self.hash_t_xml[id_3]['lemma']+'#'+self.hash_t_xml[id_t]['lemma'])
				
				if self.hash_t_xml.has_key(id_2):
					ids = self.hash_t_xml[id_2]['pos']+':'+self.hash_t_xml[id_1]['pos']+':'+self.hash_t_xml[id_t]['pos']
					if re.match('^adj:adj:(n|prop)$', ids) is not None:
						self.__addElementHashAN__('adj_#'+self.hash_t_xml[id_2]['lemma']+'#'+self.hash_t_xml[id_t]['lemma'])

				if self.hash_t_xml.has_key(id_1):
					ids = self.hash_t_xml[id_1]['pos']+':'+self.hash_t_xml[id_t]['pos']
					if re.match('^adj:(n|prop)$', ids) is not None:
						self.__addElementHashAN__('adj_#'+self.hash_t_xml[id_1]['lemma']+'#'+self.hash_t_xml[id_t]['lemma'])
	
	def __addElementHashAN__(self, relation):
		if self.hash_an.has_key(relation):
			self.hash_an[relation] += 1
		else:
			self.hash_an[relation] = 1

	""" Extract relations for nouns when they are subjects of a verb as noun phrases (NP).
	""" 
	def __extractSVRelations__(self):
		self.hash_t_cg = self.cg.getHashTerms()
		self.hash_nts = self.xml.getHashNTStructure()

		for id_t in self.hash_t_cg:
			if self.hash_t_cg[id_t]['synt'] == '@SUBJ>' and re.match("^(n|prop)$", self.hash_t_xml[id_t]['pos']):
				id_sentence = id_t.split("_")[0]
				id_word = id_t.split("_")[1]
				next_word = int(id_word) + 1
				id_next_word = id_sentence+'_'+str(next_word)
				
				while self.hash_t_cg.has_key(id_next_word):
					if 'v-' in self.hash_t_xml[id_next_word]['pos']:
						if self.hash_t_xml[id_t]['headof'] != '':
							self.__addElementHashSV__('subj_#'+self.hash_t_cg[id_next_word]['lemma']+'#'+self.hash_t_cg[id_t]['lemma'])
							nounphrase = self.__cleanStructureToNP__(self.hash_nts[self.hash_t_xml[id_t]['headof']]['structure'])
							self.__addElementHashSV__('subj_#'+self.hash_t_cg[id_next_word]['lemma']+'#'+nounphrase)
						else:
							self.__addElementHashSV__('subj_#'+self.hash_t_cg[id_next_word]['lemma']+'#'+self.hash_t_cg[id_t]['lemma'])
						break
					next_word += 1
					id_next_word = id_sentence+'_'+str(next_word)

			if self.hash_t_cg[id_t]['synt'] == '@<SUBJ':
				id_sentence = id_t.split("_")[0]
				id_word = id_t.split("_")[1]
				previous_word = int(id_word) - 1
				id_previous_word = id_sentence+'_'+str(previous_word)
				
				while self.hash_t_cg.has_key(id_previous_word):
					if 'v-' in self.hash_t_xml[id_previous_word]['pos']:
						self.__addElementHashSV__('subj_#'+self.hash_t_cg[id_previous_word]['lemma']+'#'+self.hash_t_cg[id_t]['lemma'])
						break
					previous_word -= 1
					id_previous_word = id_sentence+'_'+str(previous_word)

	def __cleanStructureToNP__(self, noun_phrase):
		np = list(noun_phrase)
		for id_t in noun_phrase:
			if re.match('^(adj|n|prop)', self.hash_t_xml[id_t]['pos']):
				break
			else:
				np.remove(id_t)

		for id_t in reversed(noun_phrase):
			if re.match('^(n|prop|adj)', self.hash_t_xml[id_t]['pos']):
				break
			else:
				np.remove(id_t)
		
		phrase = '';
		for id_t in np:
			phrase += self.hash_t_xml[id_t]['lemma']+' '
		return phrase.replace(" --", ",	").rstrip()

	def __addElementHashSV__(self, relation):
		if self.hash_sv.has_key(relation):
			self.hash_sv[relation] += 1
		else:
			self.hash_sv[relation] = 1

	""" Extract relations for nouns when they are objects of a verb as noun phrases (NP).
	"""
	#def __extractVORelations__(self):
		#print self.hash_nts

	def getHashAN(self):
		return self.hash_an

	def printHashAN(self):
		for id_an in self.hash_an:
			print id_an+' = '+str(self.hash_an[id_an])

	def getHashSV(self):
		return self.hash_sv

	def printHashSV(self):
		for id_sv in self.hash_sv:
			print id_sv+' = '+str(self.hash_sv[id_sv])
