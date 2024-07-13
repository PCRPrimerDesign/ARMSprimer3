import bioCommons
def getMaskedTemplate(snpID, lengthPcrTemplate, chro, position, nomask):
	'''
	Download the genomic sequence around the target SNP and all common SNPs in the sequence, and mask them as 'N' (to avoid using them as PCR primers)

	Output files: 
		1001.txt
		allSnps.txt
		masked.template.txt

	'''
	halfLength = int(lengthPcrTemplate / 2)
	start = int(position) - halfLength - 1
	end = int(position) + halfLength

	templateFilename = f"{snpID}/{str(lengthPcrTemplate)}.txt"

	seqFasta = bioCommons.downloadNucs(chro, start, end)
	pcrTemplate = bioCommons.PcrTemplate(bioCommons.stripSeq(seqFasta))
	bioCommons.writeFile(pcrTemplate.highlightCenter5, templateFilename)
	bioCommons.ScreenOutput.add(f"Genome sequence around {snpID} ({lengthPcrTemplate} bp) = {pcrTemplate.highlightCenter5}")
	bioCommons.ScreenOutput.add(f"Central 5 bp = {pcrTemplate.center5}")

	templateBA = bytearray(pcrTemplate.template, 'ascii')

	# snp147Common has the SNPs with more than 1% frequency
	rawSql = f"select chrom, chromStart, chromEnd, name, strand, refNCBI, refUCSC, observed, class, func, alleleFreqs from snp147Common where (chromStart BETWEEN {start} and {end}) AND (chrom = '{chro}')"
	sqlResultString, sqlResults = bioCommons.ucscGenomeBrowser(rawSql)

	bioCommons.writeFile(sqlResultString, f"{snpID}/allSnps.txt")

	# Mask SNPs with 'N', except the target SNP
	for record in sqlResults[1:-1]:
		index = int(record[2]) - start - 1
		if index != halfLength:
			templateBA[index] = ord('N')

	template = templateBA.decode('ascii')
	pcrMaskedTemplate = bioCommons.PcrTemplate(template)
	outputName = f"{snpID}/masked.template.txt"
	bioCommons.writeFile(pcrMaskedTemplate.template, outputName)

	if nomask:
		bioCommons.ScreenOutput.add("*** nomask == True, therefore common SNPs are not masked as 'n' ***")
		return(pcrTemplate)
	else:
		bioCommons.ScreenOutput.add("*** nomask == False, therefore common SNPs are masked as 'n' ***")
		return(pcrMaskedTemplate)

if __name__ == '__main__':
	snpID = 'rs6025'
	lengthPcrTemplate = 1001
	chro = 'chr1'
	position = 169549811
	nomask = False
	maskedWT = getMaskedTemplate (snpID, lengthPcrTemplate, chro, position, nomask)
	print(maskedWT.template)