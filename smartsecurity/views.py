from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http.response import StreamingHttpResponse
from .camera import VideoCamera
from django.http.response import StreamingHttpResponse
from .models import UserRegi
from .forms import RegiForm, CreatUserForm
import json
import csv
import pandas as pd
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView, CreateView, ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
#import pandas as pd
#

#info = []
@login_required(login_url='login')
def home(request):
    return render (request,'screen_live.html')#,{'infor':info})


def gen(camera):

    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()),
    content_type='multipart/x-mixed-replace; boundary=frame')



class RegiformView(CreateView):
    Model= UserRegi
    template_name = 'registration_form.html'
    form_class = RegiForm

    def post(self,request,*args, **kwargs):
        form = RegiForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect('home')

class UserListView(ListView):
    model = UserRegi
    template_name = 'user_list.html'

class UserDetailView(DetailView):
    model = UserRegi
    template_name = 'user_details.html'


def loginPage(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.info(request,"User name or password is incorrect")

    context = {}
    return render (request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def registrationPage(request):
    form = CreatUserForm()
    if request.method == 'POST':
        form = CreatUserForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request,"Account has been created for "+ user)
            return redirect('home')

    context = { "form":form }
    return render (request, 'registration_admin.html', context)


def about_us(request):
    context = {}
    return render (request, 'about_us.html', context)




def table1(request):
     df = pd.read_csv("Attendance.csv")
     json_records = df.reset_index().to_json(orient ='records')
     data = []
     data = json.loads(json_records)
     return render(request, 'databox.html', {'d': data})


def table2(request):
     df = pd.read_csv("Attendance.csv")
     json_records = df.reset_index().to_json(orient ='records')
     data = []
     data = json.loads(json_records)
     return render(request, 'screen_live.html', {'d': data})


class UserDeleteView(DeleteView):
    model =  UserRegi
    template_name = 'userdelete.html'
    success_url = reverse_lazy('user_list')


class UserUpdateView(UpdateView):
    model =  UserRegi
    template_name = 'update_user.html'
    fields = ['name','flat','phone','email','image']
    success_url = reverse_lazy('home')
