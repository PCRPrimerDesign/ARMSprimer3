'''
ARMSprimer3 is a Python3 program to design real time PCR primers for detecting single nucleotide polymorphism in human blood/tissue samples. It can be used either in clinical test development or research settings. 

Usage by example: python3 armsprimer3.py rs6025

Requirments to run the program:
	1) An Unix operating system (for example, Linux, Mac OSX, and Windows Subsystem for Linux).
	2) 'Primer3_core', 'twoBitToFa', and 'mysql' programs are installed or copied to the shell's executable search path.
	3) Create a work directory and copy armsprimer3.py, bioCommons.py, maskSNP.py, pcr.py, parameterDefault.json, parameterOverride.json, and primer3.py to the work directory. Then run the above command in the work directory.

Mandatory input: a SNP ID, such as rs6025

Optional input: the provided files "parameterDefault.json" and "parameterOverride.json" were tuned for SYBR Green real-time ARMS-PCR, "parameterOverride.json" can be modified to design other types of ARMS-PCR, such as probe-based real-time ARMS-PCR, or tetra-primer ARMS-PCR. It is adviced not to modify the "parameterDefault.json" and use it as reference. The parameters are identical to primer3_core program. Please see Primer3 manual for details. 

Output: 
	realarms.py output files
		screenOutput.txt: 

	maskSNP output files: 
		1001.txt
		allSnps.txt
		masked.template.txt

	pcr.py output files:
		masked.template.wild.txt
		masked.template.mutation.txt
		masked.template.mutationTemplate.minus2.txt
		masked.template.wtTemplate.minus2.txt
		masked.template.mutationTemplate.minus3.txt
		masked.template.wtTemplate.minus3.txt
		
	primer3.py output files:
		masked.template.mutationTemplate.minus2.txt.right.parameters.txt
		masked.template.mutationTemplate.minus2.txt.right.primer3.txt
		masked.template.mutationTemplate.minus2.txt.left.parameters.txt
		masked.template.mutationTemplate.minus2.txt.left.primer3.txt

		masked.template.wtTemplate.minus2.txt.right.parameters.txt
		masked.template.wtTemplate.minus2.txt.right.primer3.txt
		masked.template.wtTemplate.minus2.txt.left.parameters.txt
		masked.template.wtTemplate.minus2.txt.left.primer3.txt

		masked.template.mutationTemplate.minus3.txt.right.parameters.txt
		masked.template.mutationTemplate.minus3.txt.right.primer3.txt
		masked.template.mutationTemplate.minus3.txt.left.parameters.txt
		masked.template.mutationTemplate.minus3.txt.left.primer3.txt

		masked.template.wtTemplate.minus3.txt.right.parameters.txt
		masked.template.wtTemplate.minus3.txt.right.primer3.txt
		masked.template.wtTemplate.minus3.txt.left.parameters.txt
		masked.template.wtTemplate.minus3.txt.left.primer3.txt

Note #1: In case there are no primers found, you can do one of two things, or both.
	1) Relax the stringency of the parameter file "parameterOverride.json" or
	2) Not to mask the common SNPs on genomic sequence by instead running the following command
		python3 armsprimer3.py rs6025/nomask

Note #2: ARMSprimer3 was default to use human genome data 'hg38' (in function "ucscGenomeBrowser" of "bioCommons.py"), 'SNP147' (in function "findAltAllele" of "bioCommons.py"), and 'SNP147Common' (in function "getMaskedTemplate" of "maskSNP.py"). These datasets can be replaced with other species data sets to design ARMS-PCR primers for other species. 
'''
import sys, os
import bioCommons, maskSNP, pcr

# Requir input SNP ID, lengthPcrTemplate is a testing feature. Not required for now
nomask = False
if len(sys.argv) >= 2:
	if sys.argv[1].isalnum():
		snpID = sys.argv[1] # 'rs6025'
	else:
		snpID = sys.argv[1].split('/')[0]

		if sys.argv[1].split('/')[1] == 'nomask':
			nomask = True

	if len(sys.argv) >= 3:
		lengthPcrTemplate = int(sys.argv[2])
	else:
		lengthPcrTemplate = 1001
else:
	print('You need to enter an snpID\n')
	sys.exit()

# If haven't done so, create the SNP directory to same all output files
if os.path.exists(snpID):
	bioCommons.ScreenOutput.add(f"Directory '{snpID}' already exists and will contain output files")
else:
	os.system(f"mkdir {snpID}")
	bioCommons.ScreenOutput.add(f"Directory '{snpID}' is created and will contain output files")

# Go to UCSC to find the details of the input SNP, including wild type and mutation alleles, and locations on chromosomes
wtAllele, mutAllele, chro, positionSnpGenome, strand, sqlResultString = bioCommons.findAltAllele(snpID)
bioCommons.ScreenOutput.add('Details of your targeted SNP:\n')
bioCommons.ScreenOutput.add(sqlResultString)

# Go to UCSC, download the genomic sequence around the target SNP and all common SNPs in the sequence, and mask them as 'N'
pcrMaskedTemplate = maskSNP.getMaskedTemplate(snpID, lengthPcrTemplate, chro, positionSnpGenome, nomask)

# generate all templates and design primers
pcr.getAllArmsTemplates(snpID, wtAllele, mutAllele, pcrMaskedTemplate)

# Write screen output to a file
bioCommons.ScreenOutput.writeScreenOutputToFile(f"{snpID}/screenOutput.txt")
