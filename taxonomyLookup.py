#!/usr/bin/env python
# encoding: utf-8
"""
taxonomyLooku[.py
Created by Will Pearse on 2012-07-05.
Copyright (c) 2012 Imperial College london. All rights reserved.
James, hurry up and get to the hotel please :p
"""

#Modules
from Bio import Entrez #Email setup
import argparse #Command line arguments
import time #Delays
import pdb

#Functions
def findLineage(spName):
	try:
		handleSpName = Entrez.esearch(db="taxonomy", term=spName)
		resultsSpName = Entrez.read(handleSpName)
		handleSpName.close()
		handleID = Entrez.efetch(db="Taxonomy", id=resultsSpName['IdList'], retmode="xml")
		resultsSpID = Entrez.read(handleID)
		lineage = resultsSpID[0]["Lineage"].split("; ")
		lineage.append(spName)
		lineage.reverse()
		return lineage
	except:
		return ()


#Main function
def main():
	args = parser.parse_args()
	#Delays
	if args.delayDuration:
		delayDuration = int(args.delayDuration)
	else:
		delayDuration = 10
	if args.delayCount:
		delayCount = int(args.delayCount)
	else:
		delayCount = 10

	#Email
	if not args.email:
		print "ERROR: Must supply email address!"
		sys.exit()
	Entrez.email = args.email
	#Taxa list
	if not args.taxa:
		print "ERROR: Must supply taxa list!"
		sys.exit()
	taxa = []
	with open(args.taxa) as f:
		for each in f:
			taxa.append(each.strip())
	#Output check
	if not args.output:
		print "ERROR: Must supply output file name!"
		sys.exit()

	#Search through the taxa
	output = {}
	print "Beginning search..."
	locker = 0
	for taxon in taxa:
		print "..." + taxon
		output[taxon] = findLineage(taxon)
		locker += 1
		if locker == delayCount:
			print "......pausing......"
			time.sleep(delayDuration)
			locker = 0

	#Write out the taxa we have
	with open(args.output, 'w') as f:
		for key, item in output.items():
			if item:
				f.write(key + "," + ",".join(item) + "\n")
			else:
				f.write(key + ", NOTHING FOUND\n")

	#Done!


#Argument parsing and executing main function
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="taxonomyLookup - lookup taxonomy of taxa from NCBI", epilog="http://willpearse.github.com/taxonomyLookup - written by Will Pearse for the Purvis lab")
	parser.add_argument("-taxa", "-t", help="Name of taxat input file.")
	parser.add_argument("-output", "-o", help="Name of taxonomy output file.")
	parser.add_argument("-email", "-e", help="Email address to warn if going over limits.")
	parser.add_argument("-delayDuration", "-dD", help="Delay length (seconds) when pausing internet calls. Default: 10")
	parser.add_argument("-delayCount", "-dC", help="Number of searches before starting a delay. Default: 10")
	main()