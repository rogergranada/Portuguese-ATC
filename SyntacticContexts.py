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
		self.hash_t_cg = self.cg.getHashTerms()
		self.hash_nts = self.xml.getHashNTStructure()
		self.hash_an = {}
		
		self.__extractANRelations__()

	def __extractANRelations__(self):
		for id_t in self.hash_t_xml:
			if self.hash_t_xml[id_t]['pos'] == 'n' or self.hash_t_xml[id_t]['pos'] == 'prop':
				id_head = id_t.split("_")[0]
				id_p = id_t.split("_")[1]

				id_1 = id_head+'_'+str((int(id_p) + 1))
				id_2 = id_head+'_'+str((int(id_p) + 2))
				id_3 = id_head+'_'+str((int(id_p) + 3))

				if self.hash_t_xml.has_key(id_3):
					ids = self.hash_t_xml[id_t]['pos']+':'+self.hash_t_xml[id_1]['pos']+':'+self.hash_t_xml[id_2]['pos']+':'+self.hash_t_xml[id_3]['pos']
					if re.match("^(n|prop):prp:(art|num|pron-indef|pron-poss|pu):(n|prop)$", ids) is not None:
						self.__addElementHashAN__('prep_#'+self.hash_t_xml[id_3]['lemma']+'#'+self.hash_t_xml[id_t]['lemma'])
						self.__addElementHashAN__('prep_#'+self.hash_t_xml[id_t]['lemma']+'#'+self.hash_t_xml[id_3]['lemma'])
					if re.match("^(n|prop):adj:adj:adj$", ids) is not None:
						self.__addElementHashAN__('adj_#'+self.hash_t_xml[id_3]['lemma']+'#'+self.hash_t_xml[id_t]['lemma'])

				if self.hash_t_xml.has_key(id_2):
					ids = self.hash_t_xml[id_t]['pos']+':'+self.hash_t_xml[id_1]['pos']+':'+self.hash_t_xml[id_2]['pos']
					if re.match("^(n|prop):prp:(n|prop)$", ids) is not None:
						self.__addElementHashAN__('prep_#'+self.hash_t_xml[id_2]['lemma']+'#'+self.hash_t_xml[id_t]['lemma'])
						self.__addElementHashAN__('prep_#'+self.hash_t_xml[id_t]['lemma']+'#'+self.hash_t_xml[id_2]['lemma'])
					if re.match("^(n|prop):adj:adj$", ids) is not None:
						self.__addElementHashAN__('adj_#'+self.hash_t_xml[id_2]['lemma']+'#'+self.hash_t_xml[id_t]['lemma'])
				
				if self.hash_t_xml.has_key(id_1):
					ids = self.hash_t_xml[id_t]['pos']+':'+self.hash_t_xml[id_1]['pos']
					if re.match("^(n|prop):adj$", ids) is not None:
						self.__addElementHashAN__('adj_#'+self.hash_t_xml[id_1]['lemma']+'#'+self.hash_t_xml[id_t]['lemma'])
					if re.match("^(n|prop):(n|prop)$", ids) is not None:
						self.__addElementHashAN__('nn_#'+self.hash_t_xml[id_1]['lemma']+'#'+self.hash_t_xml[id_t]['lemma'])
						self.__addElementHashAN__('nn_#'+self.hash_t_xml[id_t]['lemma']+'#'+self.hash_t_xml[id_1]['lemma'])

				id_1 = id_head+'_'+str((int(id_p) - 1))
				id_2 = id_head+'_'+str((int(id_p) - 2))
				id_3 = id_head+'_'+str((int(id_p) - 3))

				if self.hash_t_xml.has_key(id_3):
					ids = self.hash_t_xml[id_3]['pos']+':'+self.hash_t_xml[id_2]['pos']+':'+self.hash_t_xml[id_1]['pos']+':'+self.hash_t_xml[id_t]['pos']
					if re.match("^adj:adj:adj:(n|prop)$", ids) is not None:
						self.__addElementHashAN__('adj_#'+self.hash_t_xml[id_3]['lemma']+'#'+self.hash_t_xml[id_t]['lemma'])
				
				if self.hash_t_xml.has_key(id_2):
					ids = self.hash_t_xml[id_2]['pos']+':'+self.hash_t_xml[id_1]['pos']+':'+self.hash_t_xml[id_t]['pos']
					if re.match("^adj:adj:(n|prop)$", ids) is not None:
						self.__addElementHashAN__('adj_#'+self.hash_t_xml[id_2]['lemma']+'#'+self.hash_t_xml[id_t]['lemma'])

				if self.hash_t_xml.has_key(id_1):
					ids = self.hash_t_xml[id_1]['pos']+':'+self.hash_t_xml[id_t]['pos']
					if re.match("^adj:(n|prop)$", ids) is not None:
						self.__addElementHashAN__('adj_#'+self.hash_t_xml[id_1]['lemma']+'#'+self.hash_t_xml[id_t]['lemma'])
	
	def __addElementHashAN__(self, relation):
		if self.hash_an.has_key(relation):
			self.hash_an[relation] += 1
		else:
			self.hash_an[relation] = 1

	def __extractSVRelations__(self):
		print self.hash_t_cg

	def __extractVORelations__(self):
		print self.hash_nts

	def getHashAN(self):
		return self.hash_an

	def printHashAN(self):
		for id_an in self.hash_an:
			print id_an+' = '+str(self.hash_an[id_an])
