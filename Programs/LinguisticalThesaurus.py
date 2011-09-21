#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import os
import re
import codecs

from SyntacticContexts import SyntacticContexts
from Parameters import Parameters
from Seeds import Seeds
from Accents import Accents

temp_folder = '../Temp/'
corpus_folder = '../Data/Corpus/Raw/'
ling_temp = temp_folder+'Linguistical/'
output_folder = '../Data/Output/'
parameters = Parameters()
dic_an = {}
dic_sv = {}
dic_vo = {}

def mainscript():
	try:
		root, dirs, files = os.walk(corpus_folder).next()[:3]
	except:
		print 'ERROR: It was not possible to open the ../Data/Corpus/Raw/ folder'
		sys.exit()

	for corpus_file in files:
		if re.match('.*xml$', corpus_file):
			corpus_filename = corpus_file.split('.')[0]
			contexts_file = SyntacticContexts(root+''+corpus_filename)
			contexts_file.writeDicAN(ling_temp+'AN/'+corpus_filename)
			contexts_file.writeDicSV(ling_temp+'SV/'+corpus_filename)
			contexts_file.writeDicVO(ling_temp+'VO/'+corpus_filename)
			
	command = "cat "+ling_temp+"AN/*.txt > "+temp_folder+"AN_tempMergedFile.txt"
	os.system(command)
	command = "cat "+ling_temp+"SV/*.txt > "+temp_folder+"SV_tempMergedFile.txt"
	os.system(command)
	command = "cat "+ling_temp+"VO/*.txt > "+temp_folder+"VO_tempMergedFile.txt"
	os.system(command)

	mergeTerms()
	buildToLinguaToolkit()

def mergeTerms():
	try:
		an_file = codecs.open(temp_folder+'AN_tempMergedFile.txt', 'r', 'utf-8')
	except IOError:
		print 'ERROR: System cannot open the '+temp_folder+'AN_tempMergedFile.txt file'
		sys.exit()

	for line in an_file:
		line = line.replace('\n','')
		terms = line.split('#')[0]+'#'+line.split('#')[1]+'#'+line.split('#')[2]
		freq = line.split('#')[3]
		if dic_an.has_key(terms):
			dic_an[terms] += int(freq)
		else:
			dic_an[terms] = int(freq)

	an_file.close()

	#try:
	#	an_file = codecs.open(temp_folder+'AN_tempMergedFile.txt', 'w', 'utf-8')
	#except IOError:
	#	print 'ERROR: System cannot open the '+temp_folder+'AN_tempMergedFile.txt file'
	#	sys.exit()
	#for terms in dic_an:
	#	an_file.write(terms+'#'+str(dic_an[terms])+'\n')
	#an_file.close()

	try:
		sv_file = codecs.open(temp_folder+'SV_tempMergedFile.txt', 'r', 'utf-8')
	except IOError:
		print 'ERROR: System cannot open the '+temp_folder+'SV_tempMergedFile.txt file'
		sys.exit()

	for line in sv_file:
		line = line.replace('\n','')
		terms = line.split('#')[0]+'#'+line.split('#')[1]+'#'+line.split('#')[2]
		freq = line.split('#')[3]
		if dic_sv.has_key(terms):
			dic_sv[terms] += int(freq)
		else:
			dic_sv[terms] = int(freq)
	sv_file.close()

	#try:
	#	sv_file = codecs.open(temp_folder+'SV_tempMergedFile.txt', 'w', 'utf-8')
	#except IOError:
	#	print 'ERROR: System cannot open the '+temp_folder+'SV_tempMergedFile.txt file'
	#	sys.exit()
	#for terms in dic_sv:
	#	sv_file.write(terms+'#'+str(dic_sv[terms])+'\n')
	#sv_file.close()

	try:
		vo_file = codecs.open(temp_folder+'VO_tempMergedFile.txt', 'r', 'utf-8')
	except IOError:
		print 'ERROR: System cannot open the '+temp_folder+'VO_tempMergedFile.txt file'
		sys.exit()

	for line in vo_file:
		line = line.replace('\n','')
		terms = line.split('#')[0]+'#'+line.split('#')[1]+'#'+line.split('#')[2]
		freq = line.split('#')[3]
		if dic_vo.has_key(terms):
			dic_vo[terms] += int(freq)
		else:
			dic_vo[terms] = int(freq)
	vo_file.close()

	#try:
	#	vo_file = codecs.open(temp_folder+'VO_tempMergedFile.txt', 'w', 'utf-8')
	#except IOError:
	#	print 'ERROR: System cannot open the '+temp_folder+'VO_tempMergedFile.txt file'
	#	sys.exit()
	#for terms in dic_vo:
	#	vo_file.write(terms+'#'+str(dic_vo[terms])+'\n')
	#vo_file.close()

	try:
		output_file = codecs.open(temp_folder+'tempMergedFile.txt', 'w', 'utf-8')
	except IOError:
		print 'ERROR: System cannot open the '+temp_folder+'tempMergedFile.txt file'
		sys.exit()
	for terms in dic_an:
		output_file.write(terms+'#'+str(dic_an[terms])+'\n')
	for terms in dic_sv:
		output_file.write(terms+'#'+str(dic_sv[terms])+'\n')
	for terms in dic_vo:
		output_file.write(terms+'#'+str(dic_vo[terms])+'\n')
	output_file.close()

def buildToLinguaToolkit():
	try:
		seeds_to_related_file = codecs.open(temp_folder+'seedsToRelated.txt', 'w', 'utf-8')
	except IOError:
		print 'ERROR: System cannot open the '+temp_folder+'seedsToRelated.txt file'
		sys.exit()
	seeds_file = Seeds()
	dic_seeds = seeds_file.getSeeds()
	dic_noun = {}

	for terms in dic_an:
		dic_noun[terms.split('#')[2]] = terms.split('#')[2]
	for terms in dic_sv:
		dic_noun[terms.split('#')[2]] = terms.split('#')[2]	
	for terms in dic_vo:
		dic_noun[terms.split('#')[2]] = terms.split('#')[2]

	for noun in dic_noun:
		for seed in dic_seeds:
			if noun != seed:
				seeds_to_related_file.write(seed+'#'+noun+'\n')

	command = "cat "+temp_folder+"seedsToRelated.txt | perl measures.perl "+temp_folder+"tempMergedFiles.txt 1 | gawk '{print $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13}' > "+temp_folder+"Similarities.txt"
	os.system(command)

def extractFullMIToThesaurus():
	accents = Accents()
	parameters = Parameters()
	max_qty_terms = parameters.getMaxQtyTerms()
	seeds = Seeds()
	dic_seeds = seeds.getSeeds()
	mi_file = Statistic(stat_temp+'IMT_FullStatisticalCorpus.txt')

	try:
		thesaurus_file = codecs.open('../Data/Output/T3/T3_Jaccard.xml', 'w', 'utf-8')
	except IOError:
		print 'ERROR: System cannot open the  file ../Data/Output/T3/T3_Jaccard.xml'
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
