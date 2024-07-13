#!/home/guohzh/miniconda3/bin/python
'''
Commonly used classes and functions for my bioinfomatics projects
'''
import subprocess, os

class ScreenOutput:
	'''
	Save all screen output and save it to a file at the end of the program
	'''
	contents = ''
	def add(c):
		'''
		Save screen output
		'''
		c += '\n'
		ScreenOutput.contents += c
		print(c)
	def writeScreenOutputToFile(filename):
		'''
		By the end of the program, all screen output will be saved to a file
		'''
		writeFile(ScreenOutput.contents, filename) 

def writeFile(contents, filename):
	'''
	A simple wrapper to write a file
	'''
	f = open(filename, 'w')
	f.write(contents)
	f.close()

def stripSeq(s):
	'''
	The first line and all the white spaces are stripped
	'''
	s1 = s.split('\n')[1:]
	return(''.join(s1))

class PcrTemplate:
	'''
	Take a wild type sequence and store it in many formats, including the central 5 nucleotides
	The central nucleotide is the SNP to be detected
	It also can mutate the template at any position (this is very convinient)
	'''
	def __init__(self, s):
		'''
		Currently, not all attributes are used
		'''
		seq = s.lower()
		center = int(len(s) / 2)
		self.upperCase = s.upper()
		self.lowerCase = s.lower()
		self.center5 = seq[center-2:center+3].upper()
		self.highlightCenter5 = seq[:center-2] + self.center5 + seq[center+3:]
		self.template = self.highlightCenter5
	def mute(self, pos, mutAllele):
		'''
		Mutate the template at a single position
		'''
		return(PcrTemplate(self.template[:pos] + mutAllele + self.template[pos+1:]))

def downloadNucs(chro, start, end):
	'''
	Download a segment of human genome
	'''
	command = f'twoBitToFa http://hgdownload.cse.ucsc.edu/gbdb/hg38/hg38.2bit stdout -seq={chro} -start={start} -end={end}'
	seqFasta = subprocess.check_output(command, shell=True).decode('ascii')
	return(seqFasta)

def complement(c):
	'''
	Given a nucleotide, find the complement nucleotide
	'''
	if c == 'a':
		return('t')
	elif c == 't':
		return('a')
	elif c == 'c':
		return('g')
	elif c == 'g':
		return('c')
	elif c == 'A':
		return('T')
	elif c == 'T':
		return('A')
	elif c == 'C':
		return('G')
	elif c == 'G':
		return('C')
	else:
		return(c)

def complementString(s):
	'''
	Given a DNA sequence, return the complement sequence
	'''
	return("".join([complement(c) for c in s]))

def ucscGenomeBrowser(rawSql):
	'''
	Given a SQL search statement, do the UCSC search, and return the results in two formats, string and matrix
	'''
	mysql = 'mysql --no-defaults -h genome-mysql.cse.ucsc.edu -u genome -A -e ' + '"' + rawSql + '"' + ' hg38'
	sqlResultString = subprocess.check_output(mysql, shell=True).decode('ascii')
	lines = sqlResultString.split('\n')
	sqlResults = [s.split('\t') for s in lines]
	return(sqlResultString, sqlResults)

def findAltAllele(snpID):
	'''
	Based on a snpID, retrieve the detailed information of the SNP, and return the essential ones
	'''
	rawSql = f"select chrom, chromStart, chromEnd, name, strand, refNCBI, refUCSC, observed, class, func, alleleFreqs from snp147 where name = '{snpID}'"
	sqlResultString, sqlResults = ucscGenomeBrowser(rawSql)
	strand = sqlResults[1][4]
	wtAllele = sqlResults[1][6].upper()
	chro = sqlResults[1][0]
	positionSnpGenome = sqlResults[1][2]
	refNCBI = sqlResults[1][5]
	listedObservedAlleles = sqlResults[1][7].upper()

	observedAlleles = complementString(listedObservedAlleles) if strand == '-' else listedObservedAlleles

	allele1 = observedAlleles[:1]
	allele2 = observedAlleles[2:3]

	mutAllele = ''
	if wtAllele == allele1:
		mutAllele = allele2
	elif wtAllele == allele2:
		mutAllele = allele1
	else:
		mutAllele = allele1

	return(wtAllele, mutAllele, chro, positionSnpGenome, strand, sqlResultString)

def armsTable(tem, alt, adjacent):
	'''
	ARMS mutation table to further destabalize the mismatch
	'''
	pair = ord(tem) + ord(alt)
	AA = ord('A') + ord('A')
	GG = ord('G') + ord('G')
	AG = ord('A') + ord('G')
	TC = ord('T') + ord('C')
	CC = ord('C') + ord('C')
	AC = ord('A') + ord('C')
	TT = ord('T') + ord('T')
	TG = ord('T') + ord('G')
	if pair == AA or pair == GG:
		if adjacent == 'A':
			return('A')
		elif adjacent == 'G':
			return('G')
		elif adjacent == 'C':
			return('A')
		else:
			return('G')
	elif pair == AG or pair == TC or pair == CC:
		if adjacent == 'A':
			return('C')
		elif adjacent == 'G':
			return('T')
		elif adjacent == 'C':
			return('A')
		else:
			return('G')
	elif pair == AC: # AC
		if adjacent == 'A':
			return('G')
		elif adjacent == 'G':
			return('A')
		elif adjacent == 'C':
			return('C')
		else:
			return('T')
	elif pair == TT:# TT
		if adjacent == 'A':
			return('C')
		elif adjacent == 'G':
			return('T')
		elif adjacent == 'C':
			return('A')
		else:
			return('G')
	elif pair == TG: # TG
		if adjacent == 'A':
			return('G')
		elif adjacent == 'G':
			return('A')
		elif adjacent == 'C':
			return('T')
		else:
			return('C') # The original table has C or T, we arbitrarily reture C
	else:
		print("somethis is wrong")				

def armsPcrTemplate(w, m, secondMutDistance):
	'''
	Based on the ARMS table, introduce the additional mutations. The output will be ready for PCR primer design.
	'''
	centerPos = int(len(m.template)/2)
	wtAllele = w.template[centerPos]
	wtAlleleCom = complement(wtAllele)
	mutAllele = m.template[centerPos]
	mutAlleleCom = complement(mutAllele)
	ajacentLeftAllele = w.template[centerPos - secondMutDistance]
	ajacentLeftAlleleCom = complement(ajacentLeftAllele)
	ajacentRightAllele = w.template[centerPos + secondMutDistance]
	ajacentRightAlleleCom = complement(ajacentRightAllele)

	wtTemForceLeftMissmatch = armsTable(wtAllele, mutAlleleCom, ajacentLeftAlleleCom)
	wtTemForceLeftMissmatchCom = complement(wtTemForceLeftMissmatch)
	ScreenOutput.add(f"Wild template (force left) = {wtAllele}, {mutAlleleCom}, {ajacentLeftAlleleCom} -> {wtTemForceLeftMissmatch} => {wtTemForceLeftMissmatch}")

	mutTemForceLeftMissmatch = armsTable(mutAllele, wtAlleleCom, ajacentLeftAlleleCom)
	mutTemForceLeftMissmatchCom = complement(mutTemForceLeftMissmatch)
	ScreenOutput.add(f"Mutation template (force left) = {mutAllele}, {wtAlleleCom}, {ajacentLeftAlleleCom} -> {mutTemForceLeftMissmatch} => {mutTemForceLeftMissmatch}")

	wtTemForceRightMissmatch = armsTable(wtAlleleCom, mutAllele, ajacentRightAllele)
	wtTemForceRightMissmatchCom = complement(wtTemForceRightMissmatch)
	ScreenOutput.add(f"Wild template (force right) = {wtAlleleCom}, {mutAllele}, {ajacentRightAllele} -> {wtTemForceRightMissmatch} => {wtTemForceRightMissmatchCom}")

	mutTemForceRightMissmatch = armsTable(mutAlleleCom, wtAllele, ajacentRightAllele)
	mutTemForceRightMissmatchCom = complement(mutTemForceRightMissmatch)
	ScreenOutput.add(f"Mutation template (force right) = {mutAlleleCom}, {wtAllele}, {ajacentRightAllele} -> {mutTemForceRightMissmatch} => {mutTemForceRightMissmatchCom}")


	wt = w.mute(centerPos - secondMutDistance, wtTemForceLeftMissmatch).mute(centerPos + secondMutDistance, wtTemForceRightMissmatchCom)
	mut = m.mute(centerPos - secondMutDistance, wtTemForceLeftMissmatch).mute(centerPos + secondMutDistance, mutTemForceRightMissmatchCom)

	return(wt, mut)

def primer3(parameters, parameterFileName, primerFileName):
	'''
	Run primer3_core
	'''
	writeFile(parameters, parameterFileName)
	os.system(f"primer3_core -output={primerFileName} -format_output -strict_tags {parameterFileName}")

if __name__ == '__main__':
	'''
	This is for debugging purpose
	'''
	snpID = 'rs6025'
	wtAllele, mutAllele, chro, positionSnpGenome, strand = findAltAllele(snpID)
	print(wtAllele, mutAllele, chro, positionSnpGenome, strand)
