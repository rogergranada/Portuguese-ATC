#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import os
import re
import codecs

from collections import defaultdict
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
	getThesaurusFromSeeds('Full')
	getThesaurusFromSeeds('Noun')

def executeMutualInformation():
	command = "count.pl --ngram 2 --window "+str(parameters.getWindowSize())+" "+stat_temp+"W"+str(parameters.getWindowSize())+"_FullStatisticalCorpus.txt "+stat_corpus+"FullStatisticalCorpus.txt"
	os.system(command)
	command = "count.pl --ngram 2 --window "+str(parameters.getWindowSize())+" "+stat_temp+"W"+str(parameters.getWindowSize())+"_NounStatisticalCorpus.txt "+stat_corpus+"NounStatisticalCorpus.txt"
	os.system(command)
	command = "statistic.pl tmi.pm -precision "+str(parameters.getMIPrecision())+" "+stat_temp+"IMT_FullStatisticalCorpus.txt "+stat_temp+"W"+str(parameters.getWindowSize())+"_FullStatisticalCorpus.txt"
	os.system(command)
	command = "statistic.pl tmi.pm -precision "+str(parameters.getMIPrecision())+" "+stat_temp+"IMT_NounStatisticalCorpus.txt "+stat_temp+"W"+str(parameters.getWindowSize())+"_NounStatisticalCorpus.txt"
	os.system(command)

def getThesaurusFromSeeds(typefile):
	dic_mi = defaultdict(dict)
	seeds = Seeds()
	list_seeds = seeds.getSeeds()

	try:
		file_mi = codecs.open(stat_temp+'IMT_'+typefile+'StatisticalCorpus.txt', 'r', 'utf-8')
	except IOError:
		print 'ERROR: System cannot open the '+stat_temp+'IMT_'+typefile+'StatisticalCorpus.txt file'
		sys.exit()

	first_line = False
	for line in file_mi:
		if first_line:
			terms, true_mi, freq_1, freq_2, freq_3, none = line.split(' ')
			term1_temp, term2_temp, rank = terms.split('<>')
			term1_type = term1_temp.split('__')[-1]
			term1 = term1_temp.split('__')[0]
			term2_type = term2_temp.split('__')[-1]
			term2 = term2_temp.split('__')[0]

			if term1 in list_seeds and term2_type == 'N':
				dic_mi[term1][term2] = true_mi				
		else:
			first_line = True

	accents = Accents()
	parameters = Parameters()
	max_qty_terms = parameters.getMaxQtyTerms()

	try:
		thesaurus_file = codecs.open('../Data/Output/T1/T1_'+typefile+'MutualInformation.xml', 'w', 'utf-8')
	except IOError:
		print 'ERROR: System cannot open the  file ../Data/Output/T1/T1_'+typefile+'MutualInformation.xml'
		sys.exit()

	thesaurus_file.write('<?xml version="1.0" encoding="UTF-8"?>\n<thesaurus>\n\t<ontology id="privacy">\n')
	for seed in dic_mi:
		qty_terms = 0
		dic_related = getOrderedNounMIForTerm(dic_mi,seed)
		if dic_related != False:
			thesaurus_file.write('\t\t<seed term_id="" term_name="'+accents.buildAccents(seed)+'" type="">\n')
			for related_term in dic_related:
				if qty_terms < max_qty_terms:
					thesaurus_file.write('\t\t\t<term id="" display="ON" similarity="'+related_term[0]+'">'+accents.buildAccents(related_term[1])+'</term>\n')
					qty_terms += 1
			thesaurus_file.write('\t\t</seed>\n')
	thesaurus_file.write('\t</ontology>\n</thesaurus>')
	thesaurus_file.close()

def getOrderedNounMIForTerm(dic_mi, seed):
	dic_terms = {}
	for related_term in dic_mi[seed]:
		if related_term != seed:
			dic_terms[dic_mi[seed][related_term]] = related_term
	dic_terms_aux = dic_terms
	return sorted(dic_terms_aux.items(), reverse=True)

if __name__ == '__main__':
	mainscript()
