#Standard Library
import subprocess
import os

#Get all SNPs from all vcf files
def extract_SNPs(individual):
	#Creates a list of all possible chromosome identifiers
	chromosomes = []
	for i in xrange(1, 23):
		chromosomes.append(str(i))
	chromosomes.append('X')

	#Parses each chromosomal vcf file using vcftools
	#Note: Chromosome list limited to first chromosome for testing purposes
	#Note: '--indv' option not working
	individual_option = '--indv ' + individual
	chromosomes = chromosomes[0]
	for chromosome in chromosomes:
		vcf_file = '/Users/Yusef/Documents/BENG182Project/vcf_analyzer/vcf_files/CMS_nonCMS_chr' + str(chromosome) + '.annotated.phased.vcf.gz'
		print vcf_file
		output_object = subprocess.Popen(['vcftools', '--gzvcf', vcf_file, '--freq', '--indv', str(individual), '-c'], stdout=subprocess.PIPE)
		
		#Creates a dictionary of SNP information
		#Key: chr#:bp
		#Values: [0]: RsID, [1]: Genotype, [2]: Phenotype
		#Note: For testing purposes, output limited to 100 lines
		SNP_dict = {}
		for line in output_object.stdout:
			line = line.strip().split('\t')
			if line[0] == 'CHROM':
				continue
			location = chromosome + ':' + str(line[1])
			SNP_dict[location] = []
			SNP_dict[location].append('RsID to be here')
			genotype = get_genotype(str(line[4]),str(line[5]))
			SNP_dict[location].append(genotype)
			SNP_dict[location].append('Phenotype to be here')
	return SNP_dict

#Get genotype of individual from allele frequency
def get_genotype(allele_freq1, allele_freq2):
	first_geno = allele_freq1.split(':')
	second_geno = allele_freq2.split(':')

	#Determine first character of genotype
	if float(first_geno[1]) == 0.0:
		first_geno = ''
	elif float(first_geno[1]) == 0.5:
		first_geno = str(first_geno[0])
	elif float(first_geno[1]) == 1.0:
		first_geno = str(first_geno[0]) + str(first_geno[0])

	#Determine second character of genotype
	if float(second_geno[1]) == 0.0:
		second_geno = ''
	elif float(second_geno[1]) == 0.5:
		second_geno = str(second_geno[0])
	elif float(second_geno[1]) == 1.0:
		second_geno = str(second_geno[0]) + str(second_geno[0])
	return first_geno + second_geno
	


