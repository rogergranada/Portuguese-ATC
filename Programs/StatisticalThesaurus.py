#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import os
import re
import codecs

from StatisticalCorpus import StatisticalCorpus
from Parameters import Parameters
from Seeds import Seeds
from Statistic import Statistic
from Accents import Accents


temp_folder = '../Temp/'
stat_corpus = '../Data/Corpus/Statistical/'
stat_temp = temp_folder+'Statistical/'
output_folder = '../Data/Output/'
parameters = Parameters()

def mainscript():
	
	StatisticalCorpus()
	executeMutualInformation()
	extractNounMIToThesaurus()
	extractFullMIToThesaurus()

def executeMutualInformation():
	command = "count.pl --ngram 2 --window "+str(parameters.getWindowSize())+" "+stat_temp+"W"+str(parameters.getWindowSize())+"_FullStatisticalCorpus.txt "+stat_corpus+"FullStatisticalCorpus.txt"
	os.system(command)
	command = "count.pl --ngram 2 --window "+str(parameters.getWindowSize())+" "+stat_temp+"W"+str(parameters.getWindowSize())+"_NounStatisticalCorpus.txt "+stat_corpus+"NounStatisticalCorpus.txt"
	os.system(command)
	command = "statistic.pl --format tmi.pm -precision "+str(parameters.getMIPrecision())+" "+stat_temp+"IMT_FullStatisticalCorpus.txt "+stat_temp+"W"+str(parameters.getWindowSize())+"_FullStatisticalCorpus.txt"
	os.system(command)
	command = "statistic.pl --format tmi.pm -precision "+str(parameters.getMIPrecision())+" "+stat_temp+"IMT_NounStatisticalCorpus.txt "+stat_temp+"W"+str(parameters.getWindowSize())+"_NounStatisticalCorpus.txt"
	os.system(command)

def extractNounMIToThesaurus():
	accents = Accents()
	parameters = Parameters()
	max_qty_terms = parameters.getMaxQtyTerms()
	seeds = Seeds()
	dic_seeds = seeds.getSeeds()
	mi_file = Statistic(stat_temp+'IMT_NounStatisticalCorpus.txt')

	try:
		thesaurus_file = codecs.open('../Data/Output/T1/T1_NounMutualInformation.xml', 'w', 'utf-8')
	except IOError:
		print 'ERROR: System cannot open the  file ../Data/Output/T1/T1_NounMutualInformation.xml'
		sys.exit()

	thesaurus_file.write('<?xml version="1.0" encoding="UTF-8"?>\n<thesaurus>\n\t<ontology id="privacy">\n')
	for seed in dic_seeds:
		qty_terms = 0
		dic_related = mi_file.getOrderedNounMIForTerm(seed)
		if dic_related != False:
			thesaurus_file.write('\t\t<seed term_id="" term_name="'+accents.buildAccents(seed)+'" type="">\n')
			for mi_related in dic_related:
				if qty_terms < max_qty_terms:
					thesaurus_file.write('\t\t\t<term id="" display="ON" similarity="'+mi_related[0]+'">'+accents.buildAccents(mi_related[1])+'</term>\n')
					qty_terms += 1
			thesaurus_file.write('\t\t</seed>\n')
	thesaurus_file.write('\t</ontology>\n</thesaurus>')
	thesaurus_file.close()

def extractFullMIToThesaurus():
	accents = Accents()
	parameters = Parameters()
	max_qty_terms = parameters.getMaxQtyTerms()
	seeds = Seeds()
	dic_seeds = seeds.getSeeds()
	mi_file = Statistic(stat_temp+'IMT_FullStatisticalCorpus.txt')

	try:
		thesaurus_file = codecs.open('../Data/Output/T1/T1_FullMutualInformation.xml', 'w', 'utf-8')
	except IOError:
		print 'ERROR: System cannot open the  file ../Data/Output/T1/T1_FullMutualInformation.xml'
		sys.exit()

	thesaurus_file.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n<thesaurus>\n\t<ontology id="privacy">\n')
	for seed in dic_seeds:
		qty_terms = 0
		dic_related = mi_file.getOrderedNounMIForTerm(seed)
		if dic_related != False:
			thesaurus_file.write('\t\t<seed term_id="" term_name="'+accents.buildAccents(seed)+'" type="">\n')
			for mi_related in dic_related:
				if qty_terms < max_qty_terms:
					thesaurus_file.write('\t\t\t<term id="" display="ON" similarity="'+mi_related[0]+'">'+accents.buildAccents(mi_related[1])+'</term>\n')
					qty_terms += 1
			thesaurus_file.write('\t\t</seed>\n')
	thesaurus_file.write('\t</ontology>\n</thesaurus>')
	thesaurus_file.close()

if __name__ == '__main__':
	mainscript()
