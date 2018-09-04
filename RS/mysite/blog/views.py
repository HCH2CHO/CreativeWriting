from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import os
import json
import random

from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from blog.models import User
from blog.models import history
from blog.models import fiction

from blog.WritingRecommend1 import *
from blog.WritingRecommend2 import *
from blog.WritingRecommend3 import *
from blog.WritingSystem import *
from blog.DataSave import *

###CWRS
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

#数据更新页面
def index(request):  
  return render_to_response("index.html")

@csrf_exempt
#添加文章后重新计算
def datadeal(request):
    for root, dirs, files in os.walk("blog\\static\\shortfiction"):
        for file in files:
            try:
                txt = open(root + '\\' + file, 'r',encoding='UTF-8')
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
    print('update finish!')
    return HttpResponse()

@csrf_exempt
#返回推荐文章列表
def ajax(request):
    content = request.POST.get('text')
    print('get text')


    allDict = {}
    allDict = getAllWords()

    ai = fTFIDF()
    ai.readFile()
    #recommend2 = ai.getfliter()  # 2为协同过滤推荐(数量不定),结构为列表

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
#获取记录并保存
def xietong(request):
    print("get return")
    name = request.POST.get('element1')
    readlist = request.POST.get('element2')
    score=request.POST.get('element3')
    print(score)

    #print(readlist)

    '''
    with open("based on user.txt", "a") as f:
        f.write(a+'\n')
    '''
    history0=history(user=name,readinglist=readlist,score=score)
    #history0 = history(readinglist=readlist, score=score)
    history0.save()

    return HttpResponse(len(readlist), content_type='application/json')

###KGRS
def update(request):
    UserDataSave()
    MovieDataSave()
    return render_to_response("KGRS.html")

def KGRS2(request):
    return render_to_response("KGRS2.html")

@csrf_exempt
def get_info(request):
    uid = request.POST.get('uid')
    #print(uid)
    try:
        user_one=UserClass.objects.get(userId=uid)
        movie_recommand=user_one.user_Recommand
        movie_history=user_one.user_History
        re_movie_list=movie_recommand.split('\t')[0:12]
        hi_movie_list=movie_history.split('\t')[0:12]

        highmovie=['3541415', '3742360', '1292052', '1295644', '1652587', '1292720', '1929463', '2131459', '1292215', '1292001']
        popular_list=[]
        recomend_list = []

        itemVo_list = []
        items1 = []
        items2 = []

        for item in highmovie:
            movie_one=MovieClass.objects.get(movieId=item)
            line=movie_one.movie_info.split(',')
            star=( 5*float(line[8])+4*float(line[9])+3*float(line[10])+2*float(line[11])+float(line[12]) )/100
            item={'name':line[0],'img_url':movie_one.movie_src,'star':star,'rating_count':line[7],'mid':movie_one.movieId}
            popular_list.append(item)

        for item in re_movie_list:
            movie_one=MovieClass.objects.get(movieId=item)
            line=movie_one.movie_info.split(',')
            star=( 5*float(line[8])+4*float(line[9])+3*float(line[10])+2*float(line[11])+float(line[12]) )/100
            item={'name':line[0],'img_url':movie_one.movie_src,'star':star,'rating_count':line[7],'mid':movie_one.movieId}
            recomend_list.append(item)

        for item in hi_movie_list[0:6]:
            movie_one = MovieClass.objects.get(movieId=item)
            line = movie_one.movie_info.split(',')
            star = (5 * float(line[8]) + 4 * float(line[9]) + 3 * float(line[10]) + 2 * float(line[11]) + float(line[12])) / 100
            item = {'name': line[0], 'img_url': movie_one.movie_src, 'star': star, 'rating_count': line[7], 'mid': movie_one.movieId}
            items1.append(item)

        for item in hi_movie_list[6:12]:
            movie_one = MovieClass.objects.get(movieId=item)
            line = movie_one.movie_info.split(',')
            star = (5 * float(line[8]) + 4 * float(line[9]) + 3 * float(line[10]) + 2 * float(line[11]) + float(line[12])) / 100
            item = {'name': line[0], 'img_url': movie_one.movie_src, 'star': star, 'rating_count': line[7], 'mid': movie_one.movieId}
            items2.append(item)
        itemVo_list.append(items1)
        itemVo_list.append(items2)

        data1={'uid':uid,'popular_list':popular_list,'recomend_list':recomend_list,'itemVo_list':itemVo_list}
        #print(data1)
        #for item in recomend_list:
        #print(item['img_url'])
        #return HttpResponse(json.dumps(data1), content_type='application/json')
        return render(request,"KGRS2.html",data1)
    except:
        return render_to_response("KGRS2.html")

@csrf_exempt
def get_movie(request):
    uid = request.POST.get('element2')
    mid = request.POST.get('element1')
    mid=mid.replace('/','')
    print(uid,mid)
    movie_one = MovieClass.objects.get(movieId=mid)
    line=movie_one.movie_info.split(',')

    relation=random.randint(0, 30)
    relation_list=["您看过与此电影相似导演的电影","您看过与此电影相似编剧的电影","您看过与此电影相似主演的电影","您看过与此电影相似类型的电影"
,"您看过与此电影相似国家的电影","您看过与此电影相似时长的电影","您看过与此电影相似标签的电影","您看过与此电影相似语言的电影"
,"该电影与你观看过的电影具有相似总部所在地","该电影与你观看过的电影具有相似创建地点","该电影与你观看过的电影具有相似亲属关系"
,"该电影与你观看过的电影具有相似籍贯","与您历史纪录主角出生地相同","该电影与你观看国籍相同","该电影与你观看过的电影同属一个系列"
,"该电影与你观看过的电影具有相同毕业院校","该电影与你观看过的电影具有相似所属洲","该电影与你观看过的电影具有相同首都"
,"该电影与你观看过的电影都涉及英皇老板","该电影与你观看过的电影都涉及政党","该电影与你观看过的电影都涉及小虎队成员","该电影与你观看过的电影有相同姓名"
,"该电影与你观看过的电影具有相同等级","该电影与你观看过的电影具有相似主导因素","猜你喜欢乐队","猜你喜欢团队合作影片"
,"根据地区为您推荐","根据友好城市为您推荐","该电影与你观看过的电影设计指导","该电影与你观看过的电影具有相同旗下艺人"
,"该电影与你观看过的电影具有相似地区","该电影与你观看过的电影具有相似流经区域","该电影与你观看过的电影具有相同所在州"
,"该电影与你观看过的电影具有相同地理位置","该电影与你观看过的电影形似","该电影与你观看过的电影具有相同制作人","该电影与你观看过的电影具有下辖地区","该电影与你观看过的电影具有相同HOT成员"]
    reason=relation_list[relation]
    itemVo={'name':line[0],'director':line[1],'scriptwriter':line[2],'players':line[3],'categories':line[4],'country':line[5],'tags':line[6],'language':line[13],'recommend_reason':reason}
    data={'itemVo':itemVo}
    print(data)
    #return render(request,'KGRS2.html',data2)
    return HttpResponse(json.dumps(data), content_type='application/json')