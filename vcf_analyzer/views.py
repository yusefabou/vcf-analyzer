#Standard Library
import subprocess

#Third-Party
from functions import rsID_to_info, output_SNP_database

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

	context = {
	'SNP_dict': SNP_dict,
	'name' : name,
	}
	return HttpResponse(template.render(context, request))
