from django.shortcuts import render
from userlist.forms import AddPatientForm
from django.http import HttpResponseRedirect
from userlist.forms import StatusChangeForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required




# Create your views here.
from .models import Patient, Doctor, AmslerGrid, Hospital

def index(request):
    """
    View function for home page of site.
    """
    num_patients=Patient.objects.all().count()
    num_doctors=Doctor.objects.all().count()
    # Available books (status = 'a')
    #num_authors=Author.objects.count()  # The 'all()' is implied by default.

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'front.html',
        context={'num_patients':num_patients,'num_doctors':num_doctors},
    )

from django.views import generic

class PatientListView(generic.ListView):
    model = Patient
    def get_queryset(self):
        return Patient.objects.filter(doctor = self.request.user)

class PatientDetailView(generic.DetailView):
    model = Patient
    paginate_by = 10

def about(request):
	return render(
		request,
		'about.html',
		)

from django.shortcuts import get_object_or_404
from datetime import datetime
@login_required
def amsler(request, pk, uid):
	res = get_object_or_404(AmslerGrid, uid=uid)
	if request.method == "POST":
		form = StatusChangeForm(request.POST, request.FILES)
		if form.is_valid():
			res.photo = form.cleaned_data['upload_photo']
			res.status = form.cleaned_data['verify_status']
			#res.save(commit=False)
			#res.verify_date = datetime.now()
			res.save()

			return HttpResponseRedirect(reverse('patient'))

	else:
         form = StatusChangeForm()


	return render(
		request,
		'amsler.html',
		{'date':res.verify_date, 'amsler_score':res.amsler_score, 'first_name':res.patient.first_name, 'last_name':res.patient.last_name, 'photo':res.photo,'fundus':res.patient.fundus_photo, 'status': res.get_status_display,
		'form': form, 'grid1':res.grid1 } )
   # return render( request, 'amsler.html', {'amsler_score':amsler_score}
   # )

from django.core.urlresolvers import reverse
@login_required
def addpatient(request):
    if request.method == "POST":
        form = AddPatientForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.doctor = request.user
            post.save()
            return HttpResponseRedirect(reverse('patient-detail', args=[str(post.id)]) )
    else:
         form = AddPatientForm()



    return render(request, 'addpatient.html', {
        'form': form,
    })

# API Definitions
from .serializers import AmslerGridSerializer

class AmslerView(APIView):
	def get(self, request):

		am_grid = AmslerGrid.objects.all()
		serializer = AmslerGridSerializer(am_grid,many=True)
		return Response(serializer.data)

	def post(self, request):
		serializer = AmslerGridSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import generics
class AmslerDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = AmslerGrid.objects.all()
	serializer_class = AmslerGridSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'amsler_list': reverse('ams_api', request=request, format=format),
    })

