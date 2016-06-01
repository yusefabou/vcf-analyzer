#Standard Library
import subprocess
import os

#Third-Party
from BCBio import GFF
from BCBio.GFF import GFFExaminer
from wikitools import wiki, category, page

#Get all SNPs from all vcf files
def extract_SNPs(individual):
	#Creates a list of all possible chromosome identifiers
	chromosomes = chromosome_list()

	#Parses each chromosomal vcf file using vcftools
	#Note: Chromosome list limited to first chromosome for testing purposes
	individual_option = '--indv ' + individual
	chromosomes = chromosomes[0]
	for chromosome in chromosomes:
		vcf_file = 'vcf_analyzer/vcf_files/CMS_nonCMS_chr' + str(chromosome) + '.annotated.phased.vcf.gz'
		output_object = subprocess.Popen(['vcftools', '--gzvcf', vcf_file, '--freq', '--indv', str(individual), '-c'], stdout=subprocess.PIPE)
		
		#Creates a dictionary of SNP information
		#Key: chr#:bp
		#Values: [0]: RsID, [1]: Genotype, [2]: Phenotype
		#Note: For testing purposes, output limited to 100 lines
		SNP_dict = {}
		i = 1
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
			i+=1
			if i > 100:
				break
	return SNP_dict

#Create dictionary of SNP information from rsID
def rsID_to_info(rsID, individual):
	#Creates a list of all possible chromosome identifiers
	chromosomes = chromosome_list()

	#Parses each chromosomal vcf file using vcftools to search for SNP given rsID
	SNP_dict = {}
	for chromosome in chromosomes:
		vcf_file = 'vcf_analyzer/vcf_files/CMS_nonCMS_chr' + str(chromosome) + '.annotated.phased.vcf.gz'
		output_object = subprocess.Popen(['vcftools', '--gzvcf', vcf_file, '--snp', rsID, '--freq', '--indv', str(individual), '-c'], stdout=subprocess.PIPE)
		
		#Creates a dictionary of SNP information
		#Key: rsID
		#Values: [0]: chr#:bp#, [1]: Genotype, [2]: Phenotype
		for line in output_object.stdout:
			line = line.strip().split('\t')
			if line[0] == 'CHROM':
				continue
			location = chromosome + ':' + str(line[1])
			SNP_dict[rsID] = []
			SNP_dict[rsID].append(location)
			genotype = get_genotype(str(line[4]),str(line[5]))
			SNP_dict[rsID].append(genotype)
			SNP_dict[rsID].append('Phenotype to be here')
		if len(SNP_dict) == 1:
			break
	return SNP_dict

#Creates a list of all possible chromosome identifiers
def chromosome_list():
	chromosomes = []
	for i in xrange(1, 23):
		chromosomes.append(str(i))
	chromosomes.append('X')
	return chromosomes

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

#Get phenotype of SNP
def genotype_to_phenotype(rsID, genotype):
	#Access the API for SNPedia.com
	site = wiki.Wiki("http://bots.snpedia.com/api.php")

	#Set up proper rsID and page name to search for
	rsID = rsID[0].upper() + rsID[1:]
	pagename = rsID + '(' + genotype[0] + ';' + genotype[1] + ')'

	#Retrieve text from page name
	pageobj = page.Page(site, pagename)
	#try:
	pagetext = pageobj.getWikiText()

	#Try switching allele position if request did not work
	#Not handling errors correctly
	# except NoPage:
	# 	pagename = rsID + '(' + genotype[1] + ';' + genotype[0] + ')'
	# 	pageobj = page.Page(site, pagename)
	# 	pagetext = pageobj.getWikiText()

	#Get summary and description of SNP
	pagetext = pagetext.split('}}')

	description = ' '.join(text for text in pagetext[1:]).strip().replace('{{', '')
	pagetext = pagetext[0].split('|')
	summary = ''
	for line in pagetext:
		if line.split('=')[0] == 'summary':
			summary = line.split('=')[1]
	return (description, summary)

#Get basic variant call stats about the individual
#[0]: Homozygous for reference 
#[1]: Heterozygous
#[2]: Homozygous for non-reference
#[3]: Total variant calls
def get_stats(individual):
	#Generate all possible chromosomes
	chromosomes = chromosome_list()

	#Parses each chromosomal vcf file using vcftools to count each statistic
	homozygous_ref = 0
	heterozygous = 0
	homozygous_alt = 0
	chromosomes = ['X']
	for chromosome in chromosomes:
		vcf_file = 'vcf_analyzer/vcf_files/CMS_nonCMS_chr' + str(chromosome) + '.annotated.phased.vcf.gz'
		output_object = subprocess.Popen(['vcftools', '--gzvcf', vcf_file, '--indv', str(individual), '--hardy', '-c'], stdout=subprocess.PIPE)
		
		#Count each occurence of the statistic
		for line in output_object.stdout:
			line = line.strip().split('\t')
			if line[0] == 'CHR':
				continue
			stats = line[2].split('/')
			if int(stats[0]) == 1:
				homozygous_ref += 1
			elif int(stats[1]) == 1:
				heterozygous += 1
			elif int(stats[2]) == 1:
				homozygous_alt += 1
	
	total = homozygous_ref + heterozygous + homozygous_alt
	return (homozygous_ref, heterozygous, homozygous_alt, total)








