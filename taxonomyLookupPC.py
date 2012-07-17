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


delayDuration = 10
delayCount = 10
Entrez.email = "EMAIL"
taxa = []
with open("INPUTFILE") as f:
        for each in f:
                taxa.append(each.strip())
#Search through the taxa
output = []
print "Beginning search..."
locker = 0
for taxon in taxa:
        print "..." + taxon
        output.append(findLineage(taxon))
        locker += 1
        if locker == delayCount:
                print "......pausing......"
                time.sleep(delayDuration)
                locker = 0

#Write out the taxa we have
with open("OUTPUTFILE", 'w') as f:
        for taxon, lineage in zip(taxa, output):
                if item:
                        f.write(taxon + "," + ",".join(lineage) + "\n")
                else:
                        f.write(taxon + ", NOTHING FOUND\n")

#Done!
