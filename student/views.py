import requests.cookies
from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse, JsonResponse
from .forms import UserForm, Register_Student_Form, Register_Teacher_Form
from student import models
import os
import re
from random import Random
from djangoProject1 import settings
from django.core.mail import send_mail
from django.core import serializers
import json
# Create your views here.

def index(request):
    if request.method == 'GET':
        return render(request, 'student/index.html', locals())
    else:
        email = request.COOKIES.get('email')
        if email:
            try:
                user = models.Student.objects.get(email=email)
            except:
                user = models.Teacher.objects.get(email=email)
            name = user.name
        return render(request, 'student/index.html', locals())

def student_login(request):
    message = ''
    if request.method == 'GET':
        login_form = UserForm()
        return render(request, 'student/log.html', locals())

    elif request.method == 'POST':
        login_form = UserForm(request.POST)
        # 判断邮箱和密码是否为空
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            try:
                try:
                    user = models.Student.objects.get(email=email)
                    identity = 'student'
                except:
                    user = models.Teacher.objects.get(email=email)
                    identity = 'teacher'

                request.session['email'] = email
                # 校验密码是否正确
                if user.password == password:
                    response = redirect('/index/')
                    response.set_cookie('email', user.email)
                    response.set_cookie('username', user.name)
                    response.set_cookie('identity', identity)
                    return response
                else:
                    message = '密码错误'
                    return render(request, 'student/log.html', locals())
            except:
                message = '用户不存在'
            return render(request, 'student/log.html', locals())

def logout(request):
    if request.method == 'GET':
        respone = redirect('/index/')
        respone.delete_cookie('username')
        respone.delete_cookie('email')
        respone.delete_cookie('identity')
        return respone

# 学生注册
def register(request):
    message = ''
    if request.method == 'GET':
        register_form = Register_Student_Form()
        return render(request, 'student/register.html', locals())
    elif request.method == 'POST':
        register_form = Register_Student_Form(request.POST)
        if register_form.is_valid():
            # 获取数据
            email = register_form.cleaned_data['email']
            student_number = register_form.cleaned_data['student_number']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            grade = register_form.cleaned_data['grade']
            name = register_form.cleaned_data['name']
            sex = register_form.cleaned_data['sex']
            major = register_form.cleaned_data['major']
            if password1 != password2:
                message = '请确认密码相同'
                return render(request, 'student/register.html', locals())
            else:
                try:
                    new_User = models.Student.objects.create()
                except:
                    message = '邮箱已经存在'
                    return render(request, 'student/register.html', locals())
                new_User.email = email
                new_User.student_number = student_number
                new_User.password = password1
                new_User.grade = grade
                new_User.sex = sex
                new_User.major = major
                new_User.name = name
                new_User.save()
                return redirect('/login/')
        else:
            message = '表单请填写完整'
        return render(request, 'student/register.html', locals())

# 教师注册
def register_t(request):
    if request.method == 'GET':
        register_form = Register_Teacher_Form()
        return render(request, 'student/teacher_register.html', locals())
    elif request.method == 'POST':
        register_form = Register_Teacher_Form(request.POST)
        message = ''
        if register_form.is_valid():
            # 获取数据
            email = register_form.cleaned_data['email']
            Teacher_number = register_form.cleaned_data['Teacher_number']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            name = register_form.cleaned_data['name']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:
                message = '请确认密码相同'
                return render(request, 'student/teacher_register.html', locals())
            else:
                try:
                    new_User = models.Teacher.objects.create()
                except:
                    message = '邮箱已经存在'
                    return render(request, 'student/teacher_register.html', locals())
                new_User.email = email
                new_User.Teacher_number = Teacher_number
                new_User.password = password1
                new_User.sex = sex
                new_User.name = name
                new_User.save()

                return redirect('/login/')
        else:
            message = '表单请填写完整'
        return render(request, 'student/teacher_register.html', locals())

def exam(request):
    questiones = models.Test_Questions.objects.filter(subject="数学")
    n = len(questiones)

    if request.method == 'GET':
        # 拿到所有要求科目的试题，并发送给前端
        return render(request, 'exam.html', locals())
    if request.method == 'POST':
        score = 0
        answer = request.POST
        # print(answer)
        # print(id)
        for i in range(n):
            # id_temp = id[i]
            if answer[str(i+1)] == questiones[i].answer:
                score = score + questiones[i].score

        return render(request, 'calGrade.html', {'score': score})

def calGrade(request):
    pass
    return render(request, 'calGrade.html')

def upload_file(request):
    if request.method == 'GET':
        return render(request, 'upload.html')
    else:
        method = request.POST.get("method")
        if method == 'first':
            obj = request.FILES.get("upload")
            message = ''
            if not obj:
                message = '请先选择文件'
                return render(request, 'upload.html', locals())

            file_Dir = os.path.join(os.getcwd()+'\static\\text\\', obj.name)
            with open(file_Dir, 'wb') as f:
                for chunk in obj.chunks():
                    f.write(chunk)
            with open(file_Dir, 'r', encoding="utf-8") as f:
                contents = f.read().strip()
                pattern = re.compile(r".*[答][案][：][A-D]")
                answer_list = re.findall(pattern, contents)
                content_list = re.split(r".*[答][案][：][A-D]", contents)
                n = len(answer_list)
                content_list.pop(n)
                title = []
                option = []
                for i in range(n):
                    content = content_list[i]
                    pattern = re.compile(r"\d\W.*")
                    title.append(re.findall(pattern, content))
                    title[i] = re.sub(r'^\d\W', '', title[i][0])
                    option.append(re.findall(r'[A-D][.].*', content))
                    models.Test_Questions.objects.create(title=title[i], optionA=option[i][0], optionB=option[i][1],
                                                         optionC=option[i][2], optionD=option[i][3], answer=answer_list[i],
                                                         subject='数学')
            return render(request, 'upload.html', locals())
        else:
            # print(request.POST)
            subject = request.POST.get("subject")
            title = request.POST.get("title")
            optionA = request.POST.get("optionA")
            optionB = request.POST.get("optionB")
            optionC = request.POST.get("optionC")
            optionD = request.POST.get("optionD")
            difficulty = request.POST.get("difficulty")
            answer = request.POST.get("answer")
            full_score = request.POST.get("full-score")
            # 创建新的对象
            new_test = models.Test_Questions.objects.create(subject=subject, title=title,
                    optionA=optionA, optionB=optionB, optionC=optionC, optionD=optionD, level=difficulty,
                    answer=answer, score=full_score)
        return render(request, 'upload.html')

#用户个人信息编辑界面
def profile_edit(request):
    if request.method == 'GET':
        username = request.COOKIES.get('username')
        if not username:
            return redirect('/login/')
        try:
            user = models.Student.objects.get(name=username)
        except:
            user = models.Teacher.objects.get(name=username)

        return render(request, 'profile_edit.html', locals())
    else:
        if request.POST:
            email = request.POST.get('email')
            username = request.POST.get('username')
            number = request.POST.getlist('number')
            sex = request.POST.get('sex')
            identity = request.COOKIES.get('identity')
            if email:
                if identity == 'teacher':
                    user = models.Teacher.objects.get(email=email)
                    user.Teacher_number = number[1]
                else:
                    user = models.Student.objects.get(email=email)
                    grade = request.POST.get('grade')
                    major = request.POST.get('major')
                    user.student_number = number[0]
                    user.grade = grade
                    user.major = major
                user.email = email
                user.name = username
                user.sex = sex
                response = HttpResponse("success")
                response.set_cookie('username', user.name)
                user.save()

                return response


# 随机验证码生成
def get_random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars)-1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
    return str

# 发送实验证码
def verify(request):
    if request.method == "GET":
        return render(request, 'register.html')
    else:
        param = request.POST
        if not param.get('random_str'):
            email = param.get('email')
            random_str = get_random_str()
            title = "考试管理系统"
            msg = ""
            email_from = settings.DEFAULT_FROM_EMAIL
            html_str = '<p>尊敬的用户您好！</p>' \
                       '<p>感谢您使用考试管理系统。</p>' \
                       '<p>您的邮箱为：%s 。邮箱验证码为：%s</p>'%(email, random_str)
            reciever = [
                email,
            ]
            send_mail(title, msg, email_from, reciever, html_message=html_str)
            return HttpResponse(json.dumps(random_str))
        else:
            valid = param.get("valid")
            random_str = param.get("random_str")
            if valid == random_str:
                return HttpResponse(json.dumps("ok"))
            else:
                return HttpResponse(json.dumps("验证码错误"))

# 配置试卷
def makepaper(request):
    if request.method == 'GET':
        return render(request, 'makepaper.html')
    else:
        subject = request.POST.get("options")
        tests = models.Test_Questions.objects.filter(subject=subject)
        print(tests)
        data = []
        for test in tests:
            json_dict = {}
            json_dict['title'] = test.title
            data.append(json_dict)
        return JsonResponse(data, safe=False)