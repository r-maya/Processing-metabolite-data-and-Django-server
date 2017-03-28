from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.utils.encoding import smart_str
from django.core.files import File

import os
import pandas as pd


def upload(request):
	
	if request.method == 'POST' and request.FILES['data_file']:
		
		data_file = request.FILES['data_file']
		f_sys = FileSystemStorage()
		f_name = f_sys.save(data_file.name, data_file)
		

		path_to_file = script(f_name)

		f = open(path_to_file, 'r')
		out_file = File(f)

		response = HttpResponse(out_file, content_type = 'csv')
		response['Content-Disposition'] = 'attachment; filename=%s' %smart_str('Solution.csv')
		response['X-sendfile'] = smart_str(path_to_file)

		return response

	
	return render(request, 'upload.html')



#script
def script(f_name):
	#	reading csv-file 
	#	one has to change the path before using this script.
	df = pd.read_csv(f_name, sep='\t')

	#	limiting the dataframe to those rows that have only "std" in it's cohort column
	#	and grouping them by Sample, Cohort and Metabolite Name and summing up the respective Intensities
	df_std = df[df['Cohort'].str.contains("std")].groupby(['Sample','Cohort','Metabolite Name'],as_index=False)['Intensity'].sum()

	#	As mentioned in the line just below the 1st table, data is restructured so as to
	#	represent Cohort and it's intensities 
	#	as that has to be done for each metabolite, I grouped the data according to Metabolite Name.
	df_std = df_std.sort(['Metabolite Name','Cohort'],ascending=[1,1])
	#At the above line there might be a warning. But, it is just a deprecation and can be ignored.

	#	added an extra column so as to flag if it is the 1st or the 2nd intensity value of the cohort (for a given Metabolite).
	#	initially I have kept all the values to "Intensity-1"
	df_std['one or two'] = "Intensity-1"


	#	then changed every other value to "Intensity-2"
	for i in range (0,len(df_std)):
	    if i%2 == 1:
	        df_std.iloc[i, df_std.columns.get_loc('one or two')] = "Intensity-2"

	#	I have pivoted the table to get the structure in the required format.
	#	Here, I have used the "one or two" column to set the columns for the pivoted table
	
	df2 = pd.pivot_table(df_std, values='Intensity', index=['Metabolite Name', 'Cohort'], columns=['one or two'])

	df2.to_csv("./output.csv", sep=',')

	path_to_file = os.path.realpath('output.csv')
	return path_to_file

#print(script("/Users/RaghuRRB/Downloads/Assignment1/Assignment1_raw_merged_quant_df (1).txt"))







