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

		self.dic_t_xml = self.xml.getDicTerms()
		self.dic_t_cg = self.cg.getDicTerms()
		self.dic_nts = self.xml.getDicNTStructure()

		self.dic_an = {}
		self.dic_sv = {}
		self.dic_vo = {}

		self.mountANRelations = True
		self.mountSVRelations = True
		self.mountVORelations = True

	def __extractANRelations__(self):
		for id_t in self.dic_t_xml:
			if self.dic_t_xml[id_t]['pos'] == 'n' or self.dic_t_xml[id_t]['pos'] == 'prop':
				id_sentence = id_t.split("_")[0]
				id_word = id_t.split("_")[1]

				id_1 = id_sentence+'_'+str((int(id_word) + 1))
				id_2 = id_sentence+'_'+str((int(id_word) + 2))
				id_3 = id_sentence+'_'+str((int(id_word) + 3))

				if self.dic_t_xml.has_key(id_3):
					ids = self.dic_t_xml[id_t]['pos']+':'+self.dic_t_xml[id_1]['pos']+':'+self.dic_t_xml[id_2]['pos']+':'+self.dic_t_xml[id_3]['pos']
					if re.match('^(n|prop):prp:(art|num|pron-indef|pron-poss|pu):(n|prop)$', ids) is not None:
						self.__addElementDicAN__('prep_#'+self.dic_t_xml[id_3]['lemma']+'#'+self.dic_t_xml[id_t]['lemma'])
						self.__addElementDicAN__('prep_#'+self.dic_t_xml[id_t]['lemma']+'#'+self.dic_t_xml[id_3]['lemma'])
					if re.match('^(n|prop):adj:adj:adj$', ids) is not None:
						self.__addElementDicAN__('adj_#'+self.dic_t_xml[id_3]['lemma']+'#'+self.dic_t_xml[id_t]['lemma'])

				if self.dic_t_xml.has_key(id_2):
					ids = self.dic_t_xml[id_t]['pos']+':'+self.dic_t_xml[id_1]['pos']+':'+self.dic_t_xml[id_2]['pos']
					if re.match('^(n|prop):prp:(n|prop)$', ids) is not None:
						self.__addElementDicAN__('prep_#'+self.dic_t_xml[id_2]['lemma']+'#'+self.dic_t_xml[id_t]['lemma'])
						self.__addElementDicAN__('prep_#'+self.dic_t_xml[id_t]['lemma']+'#'+self.dic_t_xml[id_2]['lemma'])
					if re.match('^(n|prop):adj:adj$', ids) is not None:
						self.__addElementDicAN__('adj_#'+self.dic_t_xml[id_2]['lemma']+'#'+self.dic_t_xml[id_t]['lemma'])
				
				if self.dic_t_xml.has_key(id_1):
					ids = self.dic_t_xml[id_t]['pos']+':'+self.dic_t_xml[id_1]['pos']
					if re.match('^(n|prop):adj$', ids) is not None:
						self.__addElementDicAN__('adj_#'+self.dic_t_xml[id_1]['lemma']+'#'+self.dic_t_xml[id_t]['lemma'])
					if re.match('^(n|prop):(n|prop)$', ids) is not None:
						self.__addElementDicAN__('nn_#'+self.dic_t_xml[id_1]['lemma']+'#'+self.dic_t_xml[id_t]['lemma'])
						self.__addElementDicAN__('nn_#'+self.dic_t_xml[id_t]['lemma']+'#'+self.dic_t_xml[id_1]['lemma'])

				id_1 = id_sentence+'_'+str((int(id_word) - 1))
				id_2 = id_sentence+'_'+str((int(id_word) - 2))
				id_3 = id_sentence+'_'+str((int(id_word) - 3))

				if self.dic_t_xml.has_key(id_3):
					ids = self.dic_t_xml[id_3]['pos']+':'+self.dic_t_xml[id_2]['pos']+':'+self.dic_t_xml[id_1]['pos']+':'+self.dic_t_xml[id_t]['pos']
					if re.match('^adj:adj:adj:(n|prop)$', ids) is not None:
						self.__addElementDicAN__('adj_#'+self.dic_t_xml[id_3]['lemma']+'#'+self.dic_t_xml[id_t]['lemma'])
				
				if self.dic_t_xml.has_key(id_2):
					ids = self.dic_t_xml[id_2]['pos']+':'+self.dic_t_xml[id_1]['pos']+':'+self.dic_t_xml[id_t]['pos']
					if re.match('^adj:adj:(n|prop)$', ids) is not None:
						self.__addElementDicAN__('adj_#'+self.dic_t_xml[id_2]['lemma']+'#'+self.dic_t_xml[id_t]['lemma'])

				if self.dic_t_xml.has_key(id_1):
					ids = self.dic_t_xml[id_1]['pos']+':'+self.dic_t_xml[id_t]['pos']
					if re.match('^adj:(n|prop)$', ids) is not None:
						self.__addElementDicAN__('adj_#'+self.dic_t_xml[id_1]['lemma']+'#'+self.dic_t_xml[id_t]['lemma'])
	
	def __addElementDicAN__(self, relation):
		relation = relation.lower()
		if self.dic_an.has_key(relation):
			self.dic_an[relation] += 1
		else:
			self.dic_an[relation] = 1

	""" Extract relations for nouns when they are subjects of a verb as noun phrases (NP).
	""" 
	def __extractSVRelations__(self):
		for id_t in self.dic_t_cg:
			if (self.dic_t_cg[id_t]['synt'] == '@SUBJ>' or self.dic_t_cg[id_t]['synt'] == '@N<PRED') and re.match("^(n|prop)$", self.dic_t_xml[id_t]['pos']):
				id_sentence = id_t.split("_")[0]
				id_word = id_t.split("_")[1]
				next_word = int(id_word) + 1
				id_next_word = id_sentence+'_'+str(next_word)
				
				while self.dic_t_cg.has_key(id_next_word):
					if 'v-' in self.dic_t_xml[id_next_word]['pos']:
						if self.dic_t_xml[id_t]['headof'] != '':
							self.__addElementDicSV__('subj_#'+self.dic_t_cg[id_next_word]['lemma']+'#'+self.dic_t_cg[id_t]['lemma'])
							nounphrase = self.__cleanStructureToNP__(self.dic_nts[self.dic_t_xml[id_t]['headof']]['structure'])
							self.__addElementDicSV__('subj_#'+self.dic_t_cg[id_next_word]['lemma']+'#'+nounphrase)
						else:
							self.__addElementDicSV__('subj_#'+self.dic_t_cg[id_next_word]['lemma']+'#'+self.dic_t_cg[id_t]['lemma'])
						break
					next_word += 1
					id_next_word = id_sentence+'_'+str(next_word)

			if self.dic_t_cg[id_t]['synt'] == '@<SUBJ' and re.match("^(n|prop)$", self.dic_t_xml[id_t]['pos']):
				id_sentence = id_t.split("_")[0]
				id_word = id_t.split("_")[1]
				previous_word = int(id_word) - 1
				id_previous_word = id_sentence+'_'+str(previous_word)
				
				while self.dic_t_cg.has_key(id_previous_word):
					if 'v-' in self.dic_t_xml[id_previous_word]['pos']:
						if self.dic_t_xml[id_t]['headof'] != '':
							self.__addElementDicSV__('subj_#'+self.dic_t_cg[id_previous_word]['lemma']+'#'+self.dic_t_cg[id_t]['lemma'])
							nounphrase = self.__cleanStructureToNP__(self.dic_nts[self.dic_t_xml[id_t]['headof']]['structure'])
							self.__addElementDicSV__('subj_#'+self.dic_t_cg[id_previous_word]['lemma']+'#'+nounphrase)
						else:
							self.__addElementDicSV__('subj_#'+self.dic_t_cg[id_previous_word]['lemma']+'#'+self.dic_t_cg[id_t]['lemma'])
						break
					previous_word -= 1
					id_previous_word = id_sentence+'_'+str(previous_word)

	def __addElementDicSV__(self, relation):
		relation = relation.lower()
		if self.dic_sv.has_key(relation):
			self.dic_sv[relation] += 1
		else:
			self.dic_sv[relation] = 1

	""" Extract relations for nouns when they are the object of a verb as noun phrases (NP).
	"""
	def __extractVORelations__(self):
		for id_t in self.dic_t_cg:
			if (self.dic_t_cg[id_t]['synt'] == '@<ACC' or self.dic_t_cg[id_t]['synt'] == '@PRED>') and re.match("^(n|prop)$", self.dic_t_xml[id_t]['pos']):
				id_sentence = id_t.split("_")[0]
				id_word = id_t.split("_")[1]
				previous_word = int(id_word) - 1
				id_previous_word = id_sentence+'_'+str(previous_word)
				
				while self.dic_t_cg.has_key(id_previous_word):
					if 'v-' in self.dic_t_xml[id_previous_word]['pos']:
						if self.dic_t_xml[id_t]['headof'] != '':
							self.__addElementDicVO__('obj_#'+self.dic_t_cg[id_previous_word]['lemma']+'#'+self.dic_t_cg[id_t]['lemma'])
							nounphrase = self.__cleanStructureToNP__(self.dic_nts[self.dic_t_xml[id_t]['headof']]['structure'])
							self.__addElementDicVO__('obj_#'+self.dic_t_cg[id_previous_word]['lemma']+'#'+nounphrase)
						else:
							self.__addElementDicVO__('obj_#'+self.dic_t_cg[id_previous_word]['lemma']+'#'+self.dic_t_cg[id_t]['lemma'])
						break
					previous_word -= 1
					id_previous_word = id_sentence+'_'+str(previous_word)

	def __addElementDicVO__(self, relation):
		relation = relation.lower()
		if self.dic_vo.has_key(relation):
			self.dic_vo[relation] += 1
		else:
			self.dic_vo[relation] = 1

	def __cleanStructureToNP__(self, noun_phrase):
		np = list(noun_phrase)
		for id_t in noun_phrase:
			if re.match('^(adj|n|prop)', self.dic_t_xml[id_t]['pos']):
				break
			else:
				np.remove(id_t)

		for id_t in reversed(noun_phrase):
			if re.match('^(n|prop|adj)', self.dic_t_xml[id_t]['pos']):
				break
			else:
				np.remove(id_t)
		
		phrase = '';
		for id_t in np:
			phrase += self.dic_t_xml[id_t]['lemma']+' '
		phrase = phrase.replace(' --', ',').rstrip()
		phrase = phrase.replace('-', '_')
		phrase = phrase.replace(' ', '_')
		phrase = phrase.replace(',,', ',')
		return phrase


	""" Get and Print methods
	"""

	def getDicAN(self):
		if self.mountANRelations:
			self.__extractANRelations__()
			self.mountANRelations = False
		return self.dic_an

	def printDicAN(self):
		if self.mountANRelations:
			self.__extractANRelations__()
			self.mountANRelations = False
		for id_an in self.dic_an:
			print id_an+' = '+str(self.dic_an[id_an])

	def writeDicAN(self, filename):
		try:
			output_an = open(filename, 'w')
			if self.mountANRelations:
				self.__extractANRelations__()
				self.mountANRelations = False
			for id_an in self.dic_an:
				output_an.write(id_an+'#'+str(self.dic_an[id_an])+'\n')
			output_an.close() 
		except IOError:
			print 'The system could not open the file '+filename+' to write'
			sys.exit()

	def getDicSV(self):
		if self.mountSVRelations:
			self.__extractSVRelations__()
			self.mountSVRelations = False
		return self.dic_sv

	def printDicSV(self):
		if self.mountSVRelations:
			self.__extractSVRelations__()
			self.mountSVRelations = False
		for id_sv in self.dic_sv:
			print id_sv+' = '+str(self.dic_sv[id_sv])

	def writeDicSV(self, filename):
		try:
			output_sv = open(filename, 'w')
			if self.mountSVRelations:
				self.__extractSVRelations__()
				self.mountSVRelations = False
			for id_sv in self.dic_sv:
				output_sv.write(id_sv+'#'+str(self.dic_sv[id_sv])+'\n')
			output_sv.close() 
		except IOError:
			print 'The system could not open the file '+filename+' to write'
			sys.exit()

	def getDicVO(self):
		if self.mountVORelations:
			self.__extractVORelations__()
			self.mountVORelations = False
		return self.dic_vo

	def printDicVO(self):
		if self.mountVORelations:
			self.__extractVORelations__()
			self.mountVORelations = False
		for id_vo in self.dic_vo:
			print id_vo+' = '+str(self.dic_vo[id_vo])

	def writeDicVO(self, filename):
		try:
			output_vo = open(filename, 'w')
			if self.mountVORelations:
				self.__extractVORelations__()
				self.mountVORelations = False
			for id_vo in self.dic_vo:
				output_vo.write(id_vo+'#'+str(self.dic_vo[id_vo])+'\n')
			output_vo.close() 
		except IOError:
			print 'The system could not open the file '+filename+' to write'
			sys.exit()
