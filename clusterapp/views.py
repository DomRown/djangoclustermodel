from django.core import serializers
from models import *
from django.views.generic import TemplateView
from django.shortcuts import render, render_to_response
from django.template import loader, RequestContext
from django.http import HttpResponse
from django.template.response import TemplateResponse,Template,Context
from django.shortcuts import render_to_response
import random,datetime,time



def index(request):
	template = loader.get_template('index.html')
	return render(request,'index.html')

def pured3(request):
	dataset=(request.POST.get('getset'))
	algorithm=(request.POST.get('getalg2'))
	numres=(request.POST.get('getnums'))
	klust=int(request.POST.get('getval'))

	if dataset=='IMDB - Ratings':
	 	settype="ratings"
	 	rows=Moviesall.values_list('rating_count','rating','title','genres__genre','director__fullname','actors__fullname')[:150]
	elif dataset=='Iris':
	 	settype="iris"
	 	rows=Irisall.values_list('sepal_width','sepal_length','species')[:150]
	else: return 0
	

	clusted=kmeans(rows,k=klust)

	##Context takes two variables - a dict mapping var names tovar vals
	##This var is made available then on the chart page
	context = RequestContext(request, {
		'data': json.dumps(clusted),
		'settype': json.dumps(settype), 
		'dataset':request.POST.get('getset'),
		'kclusters':request.POST.get('getval')
		})
	
	return render(request, 'scatterchart.html',context) 