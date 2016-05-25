#Standard Library
import subprocess

#Third-Party
from functions import extract_SNPs

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

	#Check if the submit button was pressed
	if request.method == 'POST':

		#Refresh page if name is empty
		if not request.POST.get('name'):
			return HttpResponse(template.render({}, request))
		else:
		#Get the name of individual if name was submitted
			name = request.POST.get('name').strip()
			SNP_dict = extract_SNPs(name)

	context = {
	'SNP_dict': SNP_dict,
	'name' : name,
	}
	return HttpResponse(template.render(context, request))
