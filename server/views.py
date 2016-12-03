from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from server.models import Bridge
from server.forms import BridgeForm,EventForm
from server.bridge import checkdir
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from server.Process import processevent

# Create your views here.

@csrf_exempt
def event(request):
    if request.method == 'POST':
        print "upload file----------------------------------------------"
        form = EventForm(request.POST, request.FILES)

        print "form  complete----------------------------------------------"
        print form
        if form.is_valid():
            print "form is valid"
            print request.FILES

            uploaded_file = request.FILES['eventfile']
            bridge_number = request.POST['bridgenumber']
            print bridge_number
            directory = checkdir (bridge_number)
            # Write the file to disk
            fout = open("%s/temp/%s" % (directory,uploaded_file.name), 'wb')
            for chunk in uploaded_file.chunks():
                fout.write(chunk)
            fout.close()
            print "temp file save complete-------------------------"
            processevent(bridge_number,directory)
        #return HttpResponseRedirect(reverse('server.views.event'))
        else:
            print "form is not valid"
            raise Http404
    else:
        form = EventForm()  # A empty, unbound form
    return render(request,
        'server/event.html',
        {'form': form},
    )

def condition(request):
    pk=int(request.GET.get('pk'))
    obj = Bridge.objects.all()
    bridge = obj[pk]
    condition = bridge.conditions
    return HttpResponse(condition)

def index(request):
    obj = Bridge.objects.all()
    return render(request, 'index.html',{'object_list':obj})

class BridgeList(LoginRequiredMixin,ListView):
    model = Bridge

class BridgeDetail(LoginRequiredMixin,DetailView):
    model = Bridge

class BridgeCreate(LoginRequiredMixin, CreateView):
    model = Bridge
    form_class = BridgeForm
    success_url = reverse_lazy('bridge_list')

class BridgeUpdate(LoginRequiredMixin, UpdateView):
    model = Bridge
    form_class = BridgeForm
    success_url = reverse_lazy('bridge_list')
