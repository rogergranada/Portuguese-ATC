#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import os
import re
import codecs

from ParseXml import ParseXml
from Accents import Accents

class StatisticalCorpus:

	def __init__(self):	
		self.corpus_folder = '../Data/Corpus/Raw/'
		self.full_corpus = '../Data/Corpus/Statistical/Full/'
		self.noun_corpus = '../Data/Corpus/Statistical/Noun/'
		self.dic_accents = {}
		self.__buildStatisticalCorpus__()
		self.firstLoadFile = True
		
		command = "cat "+self.full_corpus+"*.txt >> "+self.full_corpus+"../FullStatisticalCorpus.txt"
		os.system(command)
		command = "cat "+self.noun_corpus+"*.txt >> "+self.full_corpus+"../NounStatisticalCorpus.txt"
		os.system(command)

	def __buildStatisticalCorpus__(self):
		try:
			root, dirs, files = os.walk(self.corpus_folder).next()[:3]
		except:
			print 'ERROR: It was not possible to open the ../Data/Corpus/Raw/ folder'
			sys.exit()

		accents = Accents()
		self.dic_accents = accents.getAccents()
		for corpus_file in files:
			if re.match('.*xml$', corpus_file):
				corpus_filename = corpus_file.split('.')[0]
				xmlfile = ParseXml(root+''+corpus_file)
				dic_terms = xmlfile.getDicTerms()
				dic_nouns = xmlfile.getNouns()
				dic_verbs = xmlfile.getVerbs()

				id_sentence = 1
				id_word = 1
				id_t = 's'+str(id_sentence)+'_'+str(id_word)

				string_full = ''
				string_nouns = ''
				while dic_terms.has_key(id_t):
					while dic_terms.has_key(id_t):
						#if dic_terms[id_t]['pos'] != 'pu':
						if not re.match('^(pu|num|conj|art|prp|pron)', dic_terms[id_t]['pos']):
							lemma = self.__fixAccents__(dic_terms[id_t]['lemma'])
							if dic_nouns.has_key(id_t):
								string_nouns += lemma+'__N '
								string_full += lemma+'__N '
							elif dic_verbs.has_key(id_t):
								string_nouns += lemma+'__V '
								string_full += lemma+'__O '
							else:
								string_full += lemma+'__O '
							string_nouns = string_nouns.replace('-', '_')
							string_full = string_full.replace('-', '_')
						id_word += 1
						id_t = 's'+str(id_sentence)+'_'+str(id_word)
					id_word = 1
					id_sentence += 1
					id_t = 's'+str(id_sentence)+'_'+str(id_word)
				self.__writeCorpusFile__(corpus_filename, string_full, string_nouns)

	def __fixAccents__(self, raw_lemma):
		for cod in self.dic_accents:
			if cod in raw_lemma:
				raw_lemma = raw_lemma.replace(cod, self.dic_accents[cod])
		return raw_lemma
		

	def __writeCorpusFile__(self, corpus_filename, string_full, string_nouns):
		try:
			write_full = codecs.open(self.full_corpus+''+corpus_filename+'.txt', 'w', 'utf-8')
		except IOError:
			print 'ERROR: System cannot open the '+self.full_corpus+''+corpus_filename+'.txt file'
			sys.exit()
		try:
			write_nouns = codecs.open(self.noun_corpus+''+corpus_filename+'.txt', 'w','utf-8')
		except IOError:
			print 'ERROR: System cannot open the '+self.noun_corpus+''+corpus_filename+'.txt file'
			sys.exit()
		write_full.write(string_full)
		write_nouns.write(string_nouns)
		write_full.close()
		write_nouns.close()

