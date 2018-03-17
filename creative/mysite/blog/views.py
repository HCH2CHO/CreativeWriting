from re import search
from django.shortcuts import render
from blog.models import BlogsPost
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.http import HttpResponse, JsonResponse
import datetime
import os
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from blog.models import User
from blog.models import history
from blog.models import fiction

from blog.WritingRecommend1 import *
from blog.WritingRecommend2 import *
from blog.WritingRecommend3 import *
from blog.WritingSystem import *

import sqlite3

def index(request):  
  return render_to_response("index.html")

def current_time(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
def current_datetime(request):
    now = datetime.datetime.now()
    t = get_template('current_datetime.html')
    html = t.render({'current_date': now})
    return HttpResponse(html)


def index1(request):
    return render(request, 'add.html')
     
def add(request):
    a = request.GET['a']
    b = request.GET['b']
    a = int(a)
    b = int(b)
    return HttpResponse(str(a+b))

def getdevjson(request):
    print('get here')
    if ('key' in request.GET):
        searchkey = request.GET.get('key')
        return JsonResponse(search(searchkey))
    else:
        return HttpResponse('Sorry!')

def index2(request):
    blog_list = BlogsPost.objects.all()
    return render_to_response('index.html',{'blog_list':blog_list})

@csrf_exempt
def ajax(request):
    content = request.POST.get('text')
    print('get text')


    allDict = {}
    allDict = getAllWords()

    ai = fTFIDF()
    ai.readFile()
    recommend2 = ai.getfliter()  # 2为协同过滤推荐(数量不定),结构为列表

    result = fnGramAlgo(content)
    result.select150words()
    conRE = result.Readablility()
    articleWords, inputArticle = result.returnwords()  # 词频，字典格式  problem

    ai.calculateTFIDF(articleWords,inputArticle,allDict)  # 输入文本的100个词及权重
    recommend1 = ai.getArticle(conRE)  # 1为词频分析推荐

    at1 = sorted(recommend1, key=lambda t: t[3], reverse=True)

    #print(recommend2)

    return_json = {'result': "2121"}
    response_data = {}
    response_data['t1'] = at1[0][0]
    response_data['t2'] = at1[1][0]
    response_data['t3'] = at1[2][0]
    response_data['t4'] = at1[3][0]
    response_data['t5'] = at1[4][0]
    #print(response_data)
    s=""
    for book in range(5):
        s=s+at1[book][0]+","
    #print(s)
    return HttpResponse(s, content_type='text/plain')

@csrf_exempt
def save(request):
    a = request.POST.get('text')
    b = request.POST.get('username')
    print(b)
    userResult = User.objects.get(username=b)
    userResult.essay= a
    userResult.save()
    userResult1 = User.objects.get(username=b)
    c= userResult1.essay
    print(c)
    return HttpResponse(len(a), content_type='application/json')

@csrf_exempt
def datadeal(request):
    for root, dirs, files in os.walk("blog\\static\\shortfiction"):
        for file in files:
            try:
                txt = open(root + '\\' + file, 'r')
                content = txt.read()

                result = nGramAlgo(content)
                result.select150words()
                result.Readablility()  #文件名如果有逗号无法识别
                result.insertdb(file)
                txt.close()
            except:
                print('error1')



    ai=TFIDF()
    ai.readFile()
    ai.calculateTFIDF() #100个词及权重

    Apr=Apriori()
    Apr.calculateApriori()
    Apr.writeData()
    return HttpResponse()


@csrf_exempt
def xietong(request):
    print("get return")
    name = request.POST.get('element1')
    readlist = request.POST.get('element2')
    score=request.POST.get('element3')

    #print(readlist)
    #print(name)
    '''
    with open("based on user.txt", "a") as f:
        f.write(a+'\n')
    '''
    history0=history(user=name,readinglist=readlist,score=score)
    #history0 = history(readinglist=readlist, score=score)
    history0.save()

    return HttpResponse(len(readlist), content_type='application/json')

def pdf(request):
    return render(request, 'pdf.html')

def login(request):
    if request.method == "POST":
        uf = UserFormLogin(request.POST)
        if uf.is_valid():
            #获取表单信息
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            userResult = User.objects.filter(username=username,password=password)
            #pdb.set_trace()
            if (len(userResult)>0):
                return render_to_response('add.html',{'username':username,'operation':"登陆"})
            else:
                return render_to_response('login.html', {"errors": "用户名或者密码错误"})

    else:
        uf = UserFormLogin()
    return render_to_response("login.html",{'uf':uf})

def register(request):
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单信息
            username = uf.cleaned_data['username']
            email = uf.cleaned_data['email']
            password1 = uf.cleaned_data['password1']
            password2 = uf.cleaned_data['password2']
            filterResult = User.objects.filter(username=username)
            if len(filterResult) > 0:
                return render_to_response('register.html', {"errors": "用户名已存在"})
            else:
                errors = []
                if (password2 != password1):
                    errors.append("两次输入的密码不一致!")
                    return render_to_response('register.html', {'errors': errors})
            #将表单写入数据库
            user = User()
            user.username = username
            user.password = password1
            user.email = email
            user.save()
            #返回注册成功页面
            return render_to_response('success.html',{'username':username,'operation':"注册"})
    else:
        uf = UserForm()
    return render_to_response('register.html',{'uf':uf})

def CreativeWriting(request):
    return render_to_response("CreativeWriting.html")

def loginc(request):
    un = request.POST.get('username')
    pw = request.POST.get('password')
    print(un)
    userResult = User.objects.filter(username=un, password=pw)
    # pdb.set_trace()
    if (len(userResult) > 0):
        return render_to_response('cwrs.html', {'username': un})
    else:
        return render_to_response('CreativeWriting.html',{"errors": "Username or password is incorrect!"})

def signupc(request):
    un = request.POST.get('username1')
    em = request.POST.get('email')
    pw1 = request.POST.get('password1')
    pw2 = request.POST.get('password2')
    print(pw2)
    print(pw1)
    filterResult = User.objects.filter(username=un)
    if len(filterResult) > 0:
        return render_to_response('CreativeWriting.html', {"errors2": "Username already exists!"})
    else:
        errors = []
        if (pw2 != pw1):
            errors.append("The password entered twice is inconsistent!")
            return render_to_response('CreativeWriting.html', {'errors2': errors})
            # 将表单写入数据库
        user = User()
        user.username = un
        user.password = pw1
        user.email = em
        user.save()
        # 返回注册成功页面
        return render_to_response('CreativeWriting.html', {"errors": "registration success!"})

    return render_to_response('CreativeWriting.html')

class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password1 = forms.CharField(label='密码',widget=forms.PasswordInput())
    password2 = forms.CharField(label='确认密码',widget=forms.PasswordInput())
    email = forms.EmailField(label='电子邮件')

class UserFormLogin(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())