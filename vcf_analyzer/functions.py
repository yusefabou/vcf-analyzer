#Standard Library
import subprocess

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
		vcf_file = 'vcf_analyzer/vcf_files/CMS_nonCMS_chr' + str(chromosome) + '.annotated.phased.vcf.gz'
		output_object = subprocess.Popen(['vcftools', '--gzvcf', vcf_file, '--freq', '-c'], stdout=subprocess.PIPE)
		
		#Creates a dictionary of SNP information
		SNP_dict = {}
		for line in output_object.stdout:
			line = line.strip().split('\t')
			if line[0] == 'CHROM':
				continue
			location = chromosome + ':' + str(line[1])
			SNP_dict[location] = []
			SNP_dict[location].append('RsID to be here')
			SNP_dict[location].append(str(line[4]) + str(line[5]))
			SNP_dict[location].append('Phenotype to be here')
	return SNP_dict

