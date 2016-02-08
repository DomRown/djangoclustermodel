from django.views.generic import TemplateView
from django.shortcuts import render, render_to_response
from django.template import loader, RequestContext
from django.http import HttpResponse
from django.template.response import TemplateResponse,Template,Context
from models import Director,Actors,Movies,Genres,kmeans,norm
from .forms import NameForm, MovieForm
from django_project import wsgi
from django.shortcuts import render_to_response
import random,datetime,time
from blobs import blob1,blob2,crescent1,crescent2,circle1,circle2
 
Moviesall=Movies.objects.all()

def index(request):
	result_list = Moviesall.values('rating_count')[:10]
	template = loader.get_template('index.html')
	context = {'result_list': result_list,}
	#output = ', '.join([str(q) for q in result_list])
	return render(request,'index.html', context)


def search(request):
	rc = Moviesall.values_list('rating_count',flat=True)[:19]
	r = Moviesall.values_list('rating',flat=True)[:19]	
	#val2 = request.POST.get('getval', None)
	
	combo=((((rc[i]),(r[i]))) for i in range(len(rc)))
	raj=list(combo)	
	print raj
	html=raj
	
	#context = ({'htmo': htmo,})
	#return render(request, 'name.html', context)
	return HttpResponse(html)


def demochart(request):
	kin=int(request.POST.get('getval'))
	dset=str(request.POST.get('getset'))
	alg=str(request.POST.get('getalg'))
	
	sql=Moviesall.values_list('rating_count',flat=True).exclude(rating_count__gte=int(0))[:19]
	
	#data=[[] for i in range(len(sql))]
	
	data2=[(1,1),(1.5,2),(3,4),(5,7),(3.5,5),(4.5,5),(3.5,4.5)]
	xdata= kmeans(data2,k=kin)
	
	ydata=kmeans(data2,k=kin)
	color_list = ['#555442','#887565','#422334']

	extra_serie = {
		"tooltip": {"y_start": "", "y_end": 'Hi'},
		"color_list":color_list
	}
	chartdata = {'x': xdata, 'y1': ydata, 'extra1':extra_serie}
	charttype = "pieChart"
	chartcontainer = 'piechart_container'

	data={
		'charttype': charttype,
		'chartdata': chartdata,
		'chartcontainer':chartcontainer,
		'extra': {
			'x_is_date': False,
			'x_axis_format': '',
			'tag_script_js': True,
			'jquery_on_ready':False,
		}

	}

	return render_to_response('piechart.html',data)

def demochart2(request):
    nb_element=10
    #xdata=[ [(1,1)], [], [3.5,5], [(1.5,2),(3,4),(5,7),(4.5,5),(3.5,4.5)]]
    z=request.POST.get('getpoints')
    xdataprenorm=Moviesall.values_list('rating_count',flat=True)[:100]
    ydata1prenorm=Moviesall.values_list('rating',flat=True)[:100]
    xdata=norm(xdataprenorm)
    ydata1=norm(ydata1prenorm)
    
    print xdata,ydata1
    #kmeans(xdata,3)
   
    #ydata1 = [i * random.randint(1, 10) for i in range(nb_element)]
    #ydata2 = map(lambda x: x * 2, ydata1)
    #ydata3 = map(lambda x: x * 5, ydata1)

    kwargs1 = {'shape': 'circle','color':'green'}
    kwargs2 = {'shape': 'cross'}
    #kwargs3 = {'shape': 'triangle-up'}

    extra_serie1 = {"tooltip": {"y_start": "AAA", "y_end": " balls"}}

    chartdata = {
        'x': xdata,
        'name1': 'series 1', 'y1': ydata1, 'kwargs1': kwargs1, 'extra1': extra_serie1
        #'name2': 'series 2', 'y2': ydata2, 'kwargs2': kwargs2, 'extra2': extra_serie1,
        #'name3': 'series 3', 'y3': ydata3, 'kwargs3': kwargs3, 'extra3': extra_serie1
    }
    charttype = "scatterChart"
    chartcontainer = "scatterchart_container"
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        
    }
    return render_to_response('scatterchart.html', data)

def blobchart(request):
    #xdataprenorm=blob1
    #ydata1prenorm=Moviesall.values_list('rating',flat=True)[:100]
    xdata=[ [(1,1)], [], [3.5,5], [(1.5,2),(3,4),(5,7),(4.5,5),(3.5,4.5)]]
    ydata1=[ [(1,1)], [], [3.5,5], [(1.5,2),(3,4),(5,7),(4.5,5),(3.5,4.5)]]
    
    print xdata,ydata1
    #kmeans(xdata,3)
   
    #ydata1 = [i * random.randint(1, 10) for i in range(nb_element)]
    #ydata2 = map(lambda x: x * 2, ydata1)
    #ydata3 = map(lambda x: x * 5, ydata1)

    kwargs1 = {'shape': 'circle','color':'green'}
    kwargs2 = {'shape': 'cross'}
    #kwargs3 = {'shape': 'triangle-up'}

    extra_serie1 = {"tooltip": {"y_start": "AAA", "y_end": " balls"}}

    chartdata = {
        'x': xdata,
        'name1': 'series 1', 'y1': ydata1, 'kwargs1': kwargs1, 'extra1': extra_serie1
        #'name2': 'series 2', 'y2': ydata2, 'kwargs2': kwargs2, 'extra2': extra_serie1,
        #'name3': 'series 3', 'y3': ydata3, 'kwargs3': kwargs3, 'extra3': extra_serie1
    }
    charttype = "scatterChart"
    chartcontainer = "scatterchart_container"
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        
    }

    return render_to_response('scatterchart.html', data)

def pured3(request):
	data=[(1, 1), (1.5, 2), (3, 4), (5, 7), (3.5, 5), (4.5, 5), (3.5, 4.5)]
	bestmatches=[[0], [], [4], [1, 2, 3, 5, 6]]
	coordinates = [[data[index] for index in bestmatch] for bestmatch in bestmatches]
	newcoord=[[[1, 1]], [[3.5, 5]], [[1.5, 2], [3, 4], [5, 7], [4.5, 5], [3.5, 4.5]]]
	#json.dumps(coordinates,allow_nan=True)
	template=("<html></html>")
	##Context takes two variables - a dict mapping var names tovar vals

	context = RequestContext(request, {
		'newcoord': newcoord
		})
	
	return render(request, 'scatterchart.html',context)
