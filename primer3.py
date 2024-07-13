import os, json, bioCommons
'''
Write PCR primer design parameters to a file, and design primers

Output files:
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
'''
def designPrimers(filename):
	with open(filename) as f:
		sequence = f.read()
		halfLengthPlusOne = str(int(len(sequence) / 2 + 1))

	if os.path.exists('parameterOverride.json'):
		with open('parameterOverride.json') as f:
			paraUser = json.load(f)
	else:
		with open('parameterDefault.json') as f:
			paraUser = json.load(f)

	paraUserList = [f'{key}={value}\n' for (key, value) in paraUser.items()]
	paraUserList.sort()
	paraUserStr = ''.join(paraUserList)

	# right
	forceRightParameters = f"""SEQUENCE_ID={filename}
SEQUENCE_TEMPLATE={sequence}
SEQUENCE_FORCE_RIGHT_END={halfLengthPlusOne}
{paraUserStr}="""


	forceRightParameterFileName = filename + '.right' + '.parameters.txt'
	forceRightPrimerFileName = f"{filename}.right.primer3.txt"
	bioCommons.primer3(forceRightParameters, forceRightParameterFileName, forceRightPrimerFileName)

	with open(forceRightPrimerFileName) as f:
		oligoForceRightFileContents = f.readlines()

	bioCommons.ScreenOutput.add('=========Force Right==========')
	bioCommons.ScreenOutput.add(''.join(oligoForceRightFileContents[:7]))

	# left
	forceLeftParameters = f'''SEQUENCE_ID={filename}
SEQUENCE_TEMPLATE={sequence}
SEQUENCE_FORCE_LEFT_END={halfLengthPlusOne}
{paraUserStr}='''

	forceLeftParameterFileName = filename + ".left" + ".parameters.txt"
	forceLeftPrimerFileName = f"{filename}.left.primer3.txt"
	bioCommons.primer3(forceLeftParameters, forceLeftParameterFileName, forceLeftPrimerFileName)

	with open(forceLeftPrimerFileName) as f:
		oligoForceLeftFileContents = f.readlines()

	bioCommons.ScreenOutput.add("=========Force Left==========")
	bioCommons.ScreenOutput.add(''.join(oligoForceLeftFileContents[:7]))
