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
    subject = request.GET.get('subject')
    examtime = request.GET.get('examtime')
    questiones = models.Test_Questions.objects.filter(subject=subject)
    n = len(questiones)
    if request.method == 'GET':
        paper = models.Paper.objects.filter(subject=subject, examtime=examtime)
        # 拿到所有要求科目的试题，并发送给前端
        return render(request, 'exam.html', locals())
    if request.method == 'POST':
        username = request.COOKIES.get('username')
        student = models.Student.objects.get(name=username)
        subject = request.POST.get("subject")
        paper = models.Paper.objects.filter(subject=subject, examtime=examtime)
        question_info = models.Paper.objects.filter(subject=subject).values("pid").values(
                                "pid__Question_number", "pid__answer", "pid__score")
        score = 0
        for question in question_info:
            qid = str(question['pid__Question_number'])
            myAnswer = request.POST.get(qid)
            if myAnswer == question['pid__answer']:
                score = score + question['pid__score']
        models.Score.objects.create(sid=student, subject=subject, grade=score)
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
                    answer = answer_list[i][-1]
                    print(answer)
                    content = content_list[i]
                    pattern = re.compile(r"\d\W.*")
                    title.append(re.findall(pattern, content))
                    title[i] = re.sub(r'^\d\W', '', title[i][0])
                    option.append(re.findall(r'[A-D][.].*', content))
                    models.Test_Questions.objects.create(title=title[i], optionA=option[i][0], optionB=option[i][1],
                                                         optionC=option[i][2], optionD=option[i][3], answer=answer,
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
            json_dict['id'] = test.Question_number
            data.append(json_dict)
        return JsonResponse(data, safe=False)
#生成试卷
def create_Paper(request):
    if request.method == 'GET':
        return render(request, 'makepaper.html')
    else:
        # 获取数据
        subject = request.POST.get('subject')
        paperdate = request.POST.get('paperdate')
        papertime = request.POST.get('papertime')
        papercount = request.POST.get('papercount')
        papername = request.POST.get('papername')
        major_available = request.POST.get('major-available')
        pid = request.POST.getlist('pid')
        # 将时间格式转为YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]
        time = paperdate + ' ' + papertime
        # 获得创建试卷的老师对象
        identity = request.COOKIES.get('identity')
        username = request.COOKIES.get('username')
        if identity == 'teacher':
            teacher = models.Teacher.objects.filter(name=username).first()
            paper = models.Paper.objects.create(papername=papername, tid=teacher, subject=subject,
                                                major=major_available, examtime=time)
            paper.pid.set(pid)
            message = '试卷已经创建成功'

        else:
            message = '学生无法创建试卷'
        return render(request, 'makepaper.html', locals())

def startExam(request):
    if request.method == 'GET':
        return render(request, 'student/startExam.html', locals())
    else:
        identity = request.COOKIES.get('identity')
        if identity == 'student':
            user = getUser_info(request)
            subject = request.POST.get("options")
            papers = models.Paper.objects.filter(subject=subject)
            data = []
            for paper in papers:
                json_dict = {}
                json_dict['tid'] = paper.tid.name

                json_dict['subject'] = paper.subject
                json_dict['examtime'] = paper.examtime
                data.append(json_dict)
            print(data)
            return JsonResponse(data, safe=False)
        else:
            return render(request, 'student/startExam.html', locals())
# 获得用户身份信息
def getUser_info(request):
    username = request.COOKIES.get('username')
    identity = request.COOKIES.get('identity')
    if identity == 'teacher':
        user = models.Teacher.objects.filter(name=username)
    else:
        user = models.Student.objects.filter(name=username)
    return user

#教师查看成绩
def showExam(request):
    if request.method == 'GET':
        identity = request.COOKIES.get('identity')
        if identity == 'teacher':
            user = getUser_info(request)[0]
            paper = models.Paper.objects.filter(tid=user)
            return render(request, 'showExam.html', locals())
        else:
            message = '只有教师才可以查看成绩'
            return render(request, 'showExam.html', locals())


def showGrade(request):
    subject1 = request.GET.get('subject')
    grade = models.Score.objects.filter(subject=subject1)
    print(grade)
    data1 = models.Score.objects.filter(subject=subject1, grade__lt=60).count()
    data2 = models.Score.objects.filter(subject=subject1, grade__gte=60, grade__lt=70).count()
    data3 = models.Score.objects.filter(subject=subject1, grade__gte=70, grade__lt=80).count()
    data4 = models.Score.objects.filter(subject=subject1, grade__gte=80, grade__lt=90).count()
    data5 = models.Score.objects.filter(subject=subject1, grade__gte=90).count()

    data = {'data1': data1, 'data2': data2, 'data3': data3, 'data4': data4, 'data5': data5}
    print(data)
    return render(request, 'showGrade.html', {'grade': grade, 'data': data, 'subject': subject1})