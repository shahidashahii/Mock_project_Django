from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView

# Create your views here.

def home(request):
    if request.session.get('username'):
        QO=Question.objects.all()
        username=request.session.get('username')
        d={'username':username,'questions':QO}
        return render(request,'home.html',d)
    

    return render(request,'home.html')

def registration(request):
    UFO=UserForm()
    d={'UFO':UFO}
    if request.method=='POST':
         UFD=UserForm(request.POST)
         if UFD.is_valid():
            NSUFO=UFD.save(commit=False)
            password=UFD.cleaned_data['password']
            NSUFO.set_password(password)
            NSUFO.save()

            return HttpResponse('Registraion is done ')
         else:
            return HttpResponse('Data is not valid')


    return render(request,'registration.html',d)


def user_login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid username or password')
    return render(request,'user_login.html')

@login_required
def questions(request):
    QFO=QuestionForm()
    d={'QFO':QFO}
    if request.method=='POST':
        QD=QuestionForm(request.POST)
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        NSQO=QD.save(commit=False)
        NSQO.user=UO
        NSQO.save()
        return HttpResponse('Question uploded sucessfully')
    return render(request,'questions.html',d)

def insertanswer(request,pk):
    if request.method=='POST':
        QO=Question.objects.get(pk=pk)
        answer=request.POST['answer']
        username=request.session.get('username')
        userid=User.objects.get(username=username)
        answercreate=Answer.objects.get_or_create(user=userid,questions=QO,answers=answer)[0]
        answercreate.save()
        return HttpResponse('answer inserted sucessfully')
        
    return render(request,'insertanswer.html')

class answer_details(DetailView):
    model=Answer
    template_name='detail_answer.html'


@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
