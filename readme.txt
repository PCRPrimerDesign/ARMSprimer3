This program (ARMSprimer3 is a suit of Python3 programs, i.e. armsprimer3.py, bioCommons.py, maskSNP.py, pcr.py, and primer3.py, by Huazhang Guo, M.D., Ph.D., Department of Pathology, SLUCare Physician Group of Saint Louis University&SSM Health Care System. Email: huazhang.guo@gmail.com) is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation as long as this paragraph is included in all distribution and modifications. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. 

ARMSprimer3 is a suit of Python3 programs to design real time PCR primers for detecting single nucleotide polymorphism in human blood/tissue samples. It can be used either in clinical test development or research settings. 

Usage by example: >>> python3 armsprimer3.py rs6025

Requirments to run the program:
	1) An Unix operating system (for example, Linux, Mac OSX, and Windows Subsystem for Linux).
	2) 'Primer3_core' (primer3.org), 'twoBitToFa' (University of California, Santa Cruz), and 'mysql' (mysql.com) programs are installed or copied to the shell's executable search path.
	3) Create a work directory and copy armsprimer3.py, bioCommons.py, maskSNP.py, pcr.py, parameterDefault.json, parameterOverride.json, and primer3.py to the work directory. Then run the above command in the work directory.

Mandatory input: a SNP ID, such as rs6025

Optional input: the provided files "parameterDefault.json" and "parameterOverride.json" were tuned for SYBR Green real-time ARMS-PCR, "parameterOverride.json" can be modified to design other types of ARMS-PCR, such as probe-based real-time ARMS-PCR, or tetra-primer ARMS-PCR. It is adviced not to modify the "parameterDefault.json" and use it as reference. The parameters are identical to primer3_core program. Please see Primer3 manual for details. 

Output: 
	armsprimer3.py output files:
		"screenOutput.txt"
			all screen output while runing the programs are saved in this file

	maskSNP output files: 
		"1001.txt"
			1001 bp of DNA sequence downloaded from UCSC genome center, the target SNP is located at 501 position
		"allSnps.txt"
			List of all common SNPs in the above DNA sequence
		"masked.template.txt"
			In the DNA sequence, all common SNPs are masked off to avoid designing PCR primers there

	pcr.py output files:
		"masked.template.wild.txt"
			Masked template DNA sequence with wild allele at 501 position
		"masked.template.mutation.txt"
			Masked template DNA sequence with mutation allele at 501 position
		"masked.template.mutationTemplate.minus2.txt"
			Masked template DNA sequence with mutation allele at 501 position and additional mutations at 500 and 502 positions
		"masked.template.wtTemplate.minus2.txt"
			Masked template DNA sequence with wild type allele at 501 position and additional mutations at 500 and 502 positions
		"masked.template.mutationTemplate.minus3.txt"
			Masked template DNA sequence with mutation allele at 501 position and additional mutations at 499 and 503 positions
		"masked.template.wtTemplate.minus3.txt"
			Masked template DNA sequence with wild type allele at 501 position and additional mutations at 499 and 503 positions
		
	primer3.py output files:
		"masked.template.mutationTemplate.minus2.txt.right.parameters.txt"
			PCR primer design parameter file to force the designed right primer to be mutation allele specific at 3' end and to introduce additional mutation at -2 position
		"masked.template.mutationTemplate.minus2.txt.right.primer3.txt"
			Designed PCR primers that the right primer to be mutation allele specific at 3' end and to have additional mutation at -2 position 
		"masked.template.mutationTemplate.minus2.txt.left.parameters.txt"
			PCR primer design parameter file to force the designed left primer to be mutation allele specific at 3' end and to introduce additional mutation at -2 position
		"masked.template.mutationTemplate.minus2.txt.left.primer3.txt"
			Designed PCR primers that the left primer to be mutation allele specific at 3' end and to have additional mutation at -2 position

		"masked.template.wtTemplate.minus2.txt.right.parameters.txt"
			PCR primer design parameter file to force the designed right primer to be wild type allele specific at 3' end and to introduce additional mutation at -2 position
		"masked.template.wtTemplate.minus2.txt.right.primer3.txt"
			Designed PCR primers that the right primer to be wild type allele specific at 3' end and to have additional mutation at -2 position
		"masked.template.wtTemplate.minus2.txt.left.parameters.txt"
			PCR primer design parameter file to force the designed left primer to be wild type allele specific at 3' end and to introduce additional mutation at -2 position
		"masked.template.wtTemplate.minus2.txt.left.primer3.txt"
			Designed PCR primers that the left primer to be wild type allele specific at 3' end and to have additional mutation at -2 position

		"masked.template.mutationTemplate.minus3.txt.right.parameters.txt"
			PCR primer design parameter file to force the designed right primer to be mutation allele specific at 3' end and to introduce additional mutation at -3 position
		"masked.template.mutationTemplate.minus3.txt.right.primer3.txt"
			Designed PCR primers that the right primer to be mutation allele specific at 3' end and to have additional mutation at -3 position 
		"masked.template.mutationTemplate.minus3.txt.left.parameters.txt"
			PCR primer design parameter file to force the designed left primer to be mutation allele specific at 3' end and to introduce additional mutation at -3 position
		"masked.template.mutationTemplate.minus3.txt.left.primer3.txt"
			Designed PCR primers that the left primer to be mutation allele specific at 3' end and to have additional mutation at -3 position

		"masked.template.wtTemplate.minus3.txt.right.parameters.txt"
			PCR primer design parameter file to force the designed right primer to be wild type allele specific at 3' end and to introduce additional mutation at -3 position
		"masked.template.wtTemplate.minus3.txt.right.primer3.txt"
			Designed PCR primers that the right primer to be wild type allele specific at 3' end and to have additional mutation at -3 position 
		"masked.template.wtTemplate.minus3.txt.left.parameters.txt"
			PCR primer design parameter file to force the designed left primer to be wild type allele specific at 3' end and to introduce additional mutation at -3 position
		"masked.template.wtTemplate.minus3.txt.left.primer3.txt"
			Designed PCR primers that the left primer to be wild type allele specific at 3' end and to have additional mutation at -3 position

Note #1: 
	1) Many of the output files are useful intermediate files for manual examination or debug purposes
	2) The essential output files that contains the designed PCR primers are:
		"screenOutput.txt"
		"masked.template.mutationTemplate.minus2.txt.right.primer3.txt"
		"masked.template.mutationTemplate.minus2.txt.left.primer3.txt"
		"masked.template.wtTemplate.minus2.txt.right.primer3.txt"
		"masked.template.wtTemplate.minus2.txt.left.primer3.txt"
		"masked.template.mutationTemplate.minus3.txt.right.primer3.txt"
		"masked.template.mutationTemplate.minus3.txt.left.primer3.txt"
		"masked.template.wtTemplate.minus3.txt.right.primer3.txt"
		"masked.template.wtTemplate.minus3.txt.left.primer3.txt"
	3) The output file "screenOutput.txt" has the first set of designed PCR primers and other useful runtime informations

Note #2: In case there are no primers found, you can do one of two things, or both.
	1) Relax the stringency of the parameter file "parameterOverride.json" or
	2) Not to mask the common SNPs on genomic sequence by instead running the following command
		>>> python3 armsprimer3.py rs6025/nomask

Note #3: ARMSprimer3 was default to use human genome data 'hg38' (in function "ucscGenomeBrowser" of "bioCommons.py"), 'SNP147' (in function "findAltAllele" of "bioCommons.py"), and 'SNP147Common' (in function "getMaskedTemplate" of "maskSNP.py"). These datasets can be replaced with other species data sets to design ARMS-PCR primers for other species. 

Note #4: The validity of ARMSprimer3 was confirmed by successfully developing four diagnostic tests using ARMSprimer3 in the molecular diagnostic laboratory at Saint Louis University. (see ARMSprimer3 output files in folders rs6025, rs1799963, rs1800562, and rs1799945, at https://github.com/PCRPrimerDesign/ARMSprimer3/, for factor V Leiden, prothrombin G20210A, and hereditary hemochromatosis-related C282Y and H63D mutations detection, respectively)