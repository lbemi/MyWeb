from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from MySite import api
from MySite.models import Goods, Users, GoodsInfo
from django.db.models import Q
import json
from django.core import serializers
from MySite.forms import NameForm, ContactForm,RegisterForm, FileMailForm, TextEmailForm
from django.core.mail import send_mail,send_mass_mail
from django.core.mail import EmailMultiAlternatives
from MyWeb import settings
import os
from hashlib import md5



def index(request):
    # with open('/home/wjl/MyWeb/MySite/data', 'r', encoding='utf-8') as file:
        # for line in file:
        #     lst = line.strip().split(',')
        #     print(lst)
        #     state = GoodsInfo.objects.create(goods_name=lst[0],
        #                                  goods_number=lst[1],
        #                                  goods_price=lst[2])
        #     print(state)
    return render(request,'index.html',{'title':'首页'})

def trans2(request,from_lang,to_lang,words):
    # from_lang = request.GET['from_lang']
    # to_lang = request.GET['to_lang']
    # text = request.GET['words']
    print(words)
    print(from_lang)
    print(to_lang)
    return  HttpResponse(api.trans(from_lang=from_lang,to_lang=to_lang,query=words))

def trans(request):
    from_lang = request.GET['from_lang']
    to_lang = request.GET['to_lang']
    text = request.GET['words']
    return  HttpResponse(api.trans(from_lang=from_lang,to_lang=to_lang,query=text))

    #http://127.0.0.1:8000/trans/?from_lang=zh&to_lang=en&words=%E4%BD%9C%E8%80%85%E6%98%AF%E5%B8%85%E5%93%A5

def news_list(request,news_type):
    news_dict = {'economic': '经济', 'sport': '体育'}
    news_titles =[]
    print(news_type)
    if news_type == 'economic':
        news_titles = [('12/5', '作者成为全国首富。'), ('12/4', '作者成为全省首富。'),
                       ('12/3', '作者成为全市首富。'), ('12/2', '作者成为镇里首富。'), ('12/1', '作者成为村里首富。')]
    return render(request, 'news_list.html', {'news_type':news_dict[news_type],'news_titles':news_titles})


def fiter_test(request):
    content = {
        'title':'过滤器',
        'letters':'abc',
        'number':1
    }
    return render(request,'fiter.html',content)


def searchall(request):
    goods_list = Goods.objects.all()
    return render(request,'search_result.html',{'goods_list':goods_list,'title':'查询'})


def search_name(request):
    goods_name = request.GET['goods_name']
    print(goods_name)
    data = Goods.objects.filter(goods_name=goods_name)
    print(data)
    content = {
        'goods_list':data,
        'title':'搜索结果'
    }
    return render(request, 'search_result.html',content)

def search_price(request):
    min_price = request.GET['min_price']
    max_price = request.GET['max_price']
    data = Goods.objects.filter(goods_price__gt=min_price,goods_price__lt=max_price)
    # data = Goods.objects.filter(Q(goods_price=min_price) | Q(goods_price=max_price))
    content = {
        'goods_list':data,
        'title':'条件查询结果'
    }
    return render(request, 'search_result.html',context=content)


def search_sort(request):
    sort = {
        'all_asc':Goods.objects.order_by('goods_price'),
        'all_desc':Goods.objects.order_by('-goods_price'),
        'result_asc':Goods.objects.filter(goods_price__lt='5').order_by('goods_price')
    }
    conntent = {
        'title':'排序查询',
        'goods_list':sort[request.GET['sort']]
    }
    return render(request,'search_result.html',context=conntent)


def reg(req):

    return render(req, 'register.html')


def register(request):
    user = request.GET['user_name']
    password = request.GET['password']
    print(user)
    result = Users.objects.create(user_name=user, password=password)
    if result:
         status =200
    else:
        status = 100
    status = {'status': status}
    result = json.dumps(status)
    print('register---->result:   ' + str(result))
    return HttpResponse(result)



def check_user(request):
    print('---------->判断用户<------------')
    user = request.GET['user_name']
    user = Users.objects.filter(user_name = user)
    if user:
        status = 100
    else:
        status = 200

    print('Check---->result:   ' + str(status))
    return HttpResponse(status)

def goods_list(request):
    result = GoodsInfo.objects.all()
    content = {
        'title':'管理商品',
        'goods_list':result
    }
    return render(request, 'goods_list.html', content)


def add_goods(request):
    name = request.GET['goods_name']
    price =  request.GET['goods_price']
    number = request.GET['goods_number']
    print("*********************")
    isexist = GoodsInfo.objects.filter(goods_name=name)
    try:
        if not isexist:

            goods = GoodsInfo()
            goods.goods_name = name
            goods.goods_price = price
            goods.goods_number = number
            goods.save()
            result = 200
        else:
            result = 100
    except Exception as e:
        print('Error--->:' + str(e))
    print(result)
    return HttpResponse(result)

def del_goods(request):
    name  = request.GET['goods_name']
    goods = GoodsInfo.objects.filter(goods_name=name)
    try:
        goods.delete()
        result = 200
    except:
        result = 100
    return HttpResponse(result)


def search(request):
    min_price = request.GET['min_price']
    max_price = request.GET['max_price']
    goods = GoodsInfo.objects.filter(goods_price__gte=min_price, goods_price__lte = max_price)
    try:
        if goods:
            result = json.dumps(serializers.serialize('json',goods))
        else:
            result = 100
    except:
        result = 100
    return HttpResponse(result)


def get_name(request):
    if request.method == 'POST':
        forms = NameForm(request.POST)
        if forms.is_valid():
            return  HttpResponseRedirect('/goods_list/')
    else:
        forms = NameForm()
    return  render(request, 'name.html',{'form':forms})


def wirte_email(request):
    form = FileMailForm()
    return render(request, 'email.html', {'email_form':form})



def upload_handler(file, file_name):
    path = os.path.join(settings.BASE_DIR,'upload/')
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path+file_name, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)
    return path + file_name


def file_mail_send(subject, message, sender, addressess, file):
    emil = EmailMultiAlternatives(subject, message, sender, addressess)
    file_path = upload_handler(file, str(file))
    emil.attach_file(file_path)
    emil.send()


def send_email(request):
    if request.method=='POST':
        if request.FILES:
            email_form = FileMailForm(request.POST, request.FILES)
            file  =request.FILES['file']
        else:
            email_form = TextEmailForm(request.POST)
            file = None
        if email_form.is_valid():
            addresses = email_form.cleaned_data['addresses'].split(',')
            subject = email_form.cleaned_data['subject']
            message = email_form.cleaned_data['message']
            print(message)
            cc_myself = email_form.cleaned_data['cc_myself']
            if cc_myself:
                addresses.append(settings.EMAIL_HOST_USER)
            count = len(addresses)
            email = [subject, message, settings.DEFAULT_FROM_EMAIL, addresses]
            try:
                if file:
                    file_mail_send(*email, file)
                    file_name = '(附件：%s)' % str(file)
                else:
                    if count>1:
                        send_mass_mail((email,))
                    else:
                        send_mail(*email)
                    file_name=''
            except:
                return HttpResponse('发送失败！')

            return render(request, 'thanks.html', {'count': count, 'to': addresses, 'file': file_name})
        else:
            return HttpResponse('验证失败！')
    else:
        email_form = FileMailForm()
        return render(request, 'email.html', {'email_form': email_form})

from MySite.models import UserModel

def re(request):
    if request.method == 'POST':
        # form = RegisterForm(request.POST)
        user = UserModel(birthday='1991-12-11')
        form = RegisterForm(request.POST, instance=user)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(",,,,,,,,,,,,,,")
            try:
                new_form = form.save(commit=False)
                m = md5()
                m.update((password+email).encode('utf-8'))
                new_form.password = m.hexdigest()
                new_form.save()
                form.save_m2m()
                print('>>>>>>>>>>>>>>>')
                # form.save()
            except:
                return HttpResponse('注册失败！！！')
            return HttpResponse('注册成功！！！')
    form= RegisterForm()
    return render(request, 're.html', {'form':form})
from django import forms
# RegisterForm = forms.modelform_factory(UserModel,
#                                        fields=('email','password','age','ip'))