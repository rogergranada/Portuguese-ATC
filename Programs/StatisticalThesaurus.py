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
from Accents import Accents

temp_folder = '../Temp/'
stat_corpus = '../Data/Corpus/Statistical/'
stat_temp = temp_folder+'Statistical/'
output_folder = '../Data/Output/'
parameters = Parameters()
max_qty_terms = parameters.getMaxQtyTerms()
seeds = Seeds()
list_seeds = seeds.getSeeds()
accents = Accents()

def mainscript():
	StatisticalCorpus()
	executeMutualInformation('Full')
	executeMutualInformation('Noun')
	getThesaurusFromSeeds('Full')
	getThesaurusFromSeeds('Noun')

def executeMutualInformation(typefile):
	command = 'count.pl --ngram 2 --window '+str(parameters.getWindowSize())+' '+stat_temp+'W'+str(parameters.getWindowSize())+'_'+typefile+'StatisticalCorpus.txt '+stat_corpus+''+typefile+'StatisticalCorpus.txt'
	os.system(command)

	try:
		file_bigrams = codecs.open(stat_temp+'W'+str(parameters.getWindowSize())+'_'+typefile+'StatisticalCorpus.txt', 'r', 'utf-8')
	except IOError:
		print 'ERROR: System cannot open the '+stat_temp+'W'+str(parameters.getWindowSize())+'_'+typefile+'StatisticalCorpus.txt file'
		sys.exit()

	first_line = False
	list_bigrams = []
	quantity = 0
	for line in file_bigrams:
		if first_line:
			term1 = line.split('__')[0]
			term1_type = (line.split('<>')[0]).split('__')[1]
			term2 = (line.split('<>')[1]).split('__')[0]
			term2_type = (line.split('<>')[1]).split('__')[1]
			if term1 in list_seeds and term1 != term2 and term1_type == 'N' and term2_type == 'N':
				list_bigrams.append(line)				
		else:
			quantity = line
			first_line = True
	file_bigrams.close()

	try:
		file_bigrams = codecs.open(stat_temp+'W'+str(parameters.getWindowSize())+'_'+typefile+'StatisticalCorpus.txt', 'w', 'utf-8')
	except IOError:
		print 'ERROR: System cannot open the '+stat_temp+'W'+str(parameters.getWindowSize())+'_'+typefile+'StatisticalCorpus.txt file'
		sys.exit()
	
	file_bigrams.write(quantity)
	for line in list_bigrams:
		file_bigrams.write(line)
	file_bigrams.close()
	

	command = "statistic.pl tmi.pm -precision "+str(parameters.getMIPrecision())+' '+stat_temp+'IMT_'+typefile+'StatisticalCorpus.txt '+stat_temp+'W'+str(parameters.getWindowSize())+'_'+typefile+'StatisticalCorpus.txt'
	os.system(command)

def getThesaurusFromSeeds(typefile):
	dic_mi = defaultdict(dict)

	try:
		file_mi = codecs.open(stat_temp+'IMT_'+typefile+'StatisticalCorpus.txt', 'r', 'utf-8')
	except IOError:
		print 'ERROR: System cannot open the '+stat_temp+'IMT_'+typefile+'StatisticalCorpus.txt file'
		sys.exit()

	first_line = False
	list_used_seeds = []
	for line in file_mi:
		if first_line:
			terms, true_mi, freq_1, freq_2, freq_3, none = line.split(' ')
			seed_temp, term_temp, rank = terms.split('<>')
			seed = seed_temp.split('__')[0]
			term = term_temp.split('__')[0]
			if seed not in list_used_seeds:
				list_used_seeds.append(seed)
				dic_mi[seed] = {'terms': []}
			dic_mi[seed]['terms'].append({term:true_mi})		
		else:
			first_line = True

	try:
		thesaurus_file = codecs.open('../Data/Output/T1/T1_'+typefile+'MutualInformation.xml', 'w', 'utf-8')
	except IOError:
		print 'ERROR: System cannot open the  file ../Data/Output/T1/T1_'+typefile+'MutualInformation.xml'
		sys.exit()

	thesaurus_file.write('<?xml version="1.0" encoding="UTF-8"?>\n<thesaurus>\n\t<ontology id="privacy">\n')

	for seed in dic_mi:
		qty_terms = 0
		thesaurus_file.write('\t\t<seed term_id="" term_name="'+accents.buildAccents(seed)+'" type="">\n')
		for index_related_term in dic_mi[seed]['terms']:
			if qty_terms < max_qty_terms:
				thesaurus_file.write('\t\t\t<term id="" display="ON" similarity="'+index_related_term[index_related_term.keys()[0]]+'">'+accents.buildAccents(index_related_term.keys()[0])+'</term>\n')
				qty_terms += 1
		thesaurus_file.write('\t\t</seed>\n')
	thesaurus_file.write('\t</ontology>\n</thesaurus>')
	thesaurus_file.close()

if __name__ == '__main__':
	mainscript()
