from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
import json
from main import models
import hashlib
import os
from django.http import HttpResponseRedirect

TYPE = ''

def test(request):
    return render(request,'test.html')

def mobilemain(request):
    return render(request,'mobilemainpage.html')

def mainpage(request):
    return render(request,'mainpage.html')

def login(request):
    return render(request,'login.html')
# Create your views here.

# def type(request):
#     if request.method == 'POST':
#         print(request.POST)
#         if request.POST['type'] == 'mobile':
#             TYPE = 'mobile'
#             return redirect('/')
#         else:
#             TYPE = 'notmobile'
#             return redirect('/')


def loginout(request):
    if request.method=='POST':
        response = HttpResponse('LOGINOUT')
        response.delete_cookie('username')
        return response
    elif request.method == 'GET':
        return HttpResponseRedirect('/')


def mobilepersonalist(request):
    # username = request.COOKIES.get('username')
    # return render('personalist.html' ,{'username':username})
    if request.method == 'GET':
        if request.COOKIES.get('username'):
            return render(request,'mobilepersonalist.html',context={'a':TYPE})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def personalist(request):
    # username = request.COOKIES.get('username')
    # return render('personalist.html' ,{'username':username})
    if request.method == 'GET':
        if request.COOKIES.get('username'):
            return render(request,'personalist.html',context={'a':TYPE})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def confirmapi(request):
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get('username') and request.POST.get('password'):
            print(11111)
            print(request.POST.get('username'))
            print(request.POST.get('password'))
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username = username,password=password)
            if user is not None:
                if user.is_active:
                    user_obj = models.Profile.objects.get(user__username=username)
                    user_list = list(user_obj.line_set.all().values('num'))
                    num_list = []
                    for item in user_list:
                        num_list.append(item['num'])
                    token = hashlib.sha1(os.urandom(24)).hexdigest()
                    print("User is valid, active and authenticated")
                    context = {'status':'1','line':num_list,'token':token}
                    response = HttpResponse({json.dumps(context)})
                    response.set_cookie('username',username,3600)
                    return response
                else:
                    print("The password is valid, but the account has been disabled!")
                    return HttpResponse({json.dumps({'status':'2'})})
            else:
                print("The username and password were incorrect.")
                return HttpResponse({json.dumps({'status':'3'})})
        else:
            print('出现未知错误')
            return HttpResponse({json.dumps({'status':4})})