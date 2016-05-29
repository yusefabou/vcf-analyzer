#Standard Library
import subprocess

#Third-Party
from functions import rsID_to_info, genotype_to_phenotype

#Django
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

#Home page 
def index(request):
	#Load the homepage template and context variables
	template = loader.get_template('vcf_analyzer/index.html')
	SNP_dict = ''
	name = ''
	rsID = ''
	summary = ''
	description = ''

	#Check if the submit button was pressed
	if request.method == 'POST':

		#Refresh page if name is empty
		if not request.POST.get('name'):
			return HttpResponse(template.render({}, request))
		else:
			#Get the name of individual and rsID
			name = request.POST.get('name').strip()
			rsID = request.POST.get('rsID').strip().lower()

			#Retrieve SNP information given rsID and individual
			SNP_dict = rsID_to_info(rsID, name)
			if SNP_dict:
				genotype = SNP_dict[rsID][1]
				phenotype = genotype_to_phenotype(rsID, genotype)
				description = phenotype[0]
				summary = phenotype[1]
			else:
				description = "No results for " + rsID + " found"

	context = {
	'SNP_dict': SNP_dict,
	'name' : name,
	'summary' : summary,
	'description' : description,
	}
	return HttpResponse(template.render(context, request))
