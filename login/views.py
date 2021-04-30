# login/views.py

from django.shortcuts import render, redirect
from . import models
from .forms import UserForm, RegisterForm, AskForm, FindbackForm, AnswerForm
import hashlib


def index(request):
    return render(request, 'login/index.html')


def questionlist(request):
    result = models.Question.objects.all()
    return render(request, 'login/questionlist.html', locals())


def search(request):
    keyStr = request.GET.get('mykey')
    result = models.Question.objects.filter(content__icontains=keyStr)
    return render(request, 'login/questionlist.html', locals())


def question(request, qid):
    query = models.Question.objects.get(id=qid)
    answerlist = models.Answer.objects.filter(query=query)
    return render(request, 'login/question.html', locals())


def delquestion(request, qid):
    if request.session['user_id'] != models.Question.objects.get(
            id=qid).creator.id:
        return redirect("/questionlist/")  # 非提问者无法删除
    models.Question.objects.filter(id=qid).delete()
    return render(request, 'login/questionlist.html',
                  {'result': models.Question.objects.all()})


def delanswer(request, qid, aid):
    if request.session['user_id'] != models.Answer.objects.get(
            id=aid).author.id:
        return redirect("/question/{{qid}}")  # 非答主无法删除
    models.Answer.objects.filter(id=aid).delete()
    query = models.Question.objects.get(id=qid)
    answerlist = models.Answer.objects.filter(query=query)
    return render(request, 'login/question.html', locals())


def ranking(request):
    return render(request, 'login/ranking.html',
                  {'result': models.User.objects.all()})


def ask(request):
    if not request.session.get('is_login', None):
        return redirect("/questionlist/")  # 未登录不允许提问
    if request.method == "POST":
        ask_form = AskForm(request.POST)
        message = "请检查填写的内容！"
        if ask_form.is_valid():  # 获取数据
            content = ask_form.cleaned_data['content']
            description = ask_form.cleaned_data['description']
            creator = models.User.objects.get(id=request.session['user_id'])

            if not content.endswith(('？', '?')):  # 判断是否以问号结尾
                message = "问题必须以问号结尾！"
                return render(request, 'login/ask.html', locals())

            # 当一切都OK的情况下，创建新问题
            new_question = models.Question.objects.create(
                content=content, description=description, creator=creator)
            creator.rating = creator.rating + 1
            creator.save()
            return redirect('/questionlist/')  # 自动跳转到问题列表页面
    ask_form = AskForm()
    return render(request, 'login/ask.html', locals())


def answer(request, qid):
    query = models.Question.objects.get(id=qid)
    author = models.User.objects.get(id=request.session['user_id'])
    if not request.session.get('is_login', None):
        return redirect("/question/%d/" % qid)  # 未登录不允许回答
    if request.method == "POST":
        answer_form = AnswerForm(request.POST)
        message = "请检查填写的内容！"
        if answer_form.is_valid():
            content = answer_form.cleaned_data['content']

            # 当一切都OK的情况下，创建新回答
            new_answer = models.Answer.objects.create(content=content,
                                                      query=query,
                                                      author=author)
            author.rating = author.rating + 3
            author.save()
            return redirect('/question/%d/' % qid)  # 自动跳转到问题页面
    answer_form = AnswerForm()
    return render(request, 'login/answer.html', locals())


def about(request):
    return render(request, 'login/about.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):  # 哈希值和数据库内的值进行比对
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create(
                    name=username,
                    password=hash_code(password1),
                    email=email,
                    sex=sex)

                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def findback(request):
    if request.session.get('is_login', None):
        # 登录状态不允许找回密码
        return redirect("/index/")
    if request.method == "POST":
        findback_form = FindbackForm(request.POST)
        message = "请检查填写的内容！"
        if findback_form.is_valid():  # 获取数据
            username = findback_form.cleaned_data['username']
            email = findback_form.cleaned_data['email']
            password1 = findback_form.cleaned_data['password1']
            password2 = findback_form.cleaned_data['password2']
            try:
                target_user = models.User.objects.get(name=username)
            except:
                message = '用户不存在，请检查用户名！'
                return render(request, 'login/findback.html', locals())
            if email != target_user.email:
                message = '邮箱错误，请检查邮箱！'
                return render(request, 'login/findback.html', locals())
            elif password1 != password2:  # 判断两次密码是否相同
                message = '两次输入的密码不同！'
                return render(request, 'login/findback.html', locals())
            else:  # 当一切都OK的情况下，修改密码
                target_user.password = hash_code(password1)
                target_user.save()
                message = '密码修改成功！'
                return redirect('/login/')  # 自动跳转到登录页面
    findback_form = FindbackForm()
    return render(request, 'login/findback.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/index/')
    request.session.flush()

    return redirect('/index/')


def hash_code(s, salt='mysite_login'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()
