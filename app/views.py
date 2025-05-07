from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Tag, Profile, Question, Answer, AnswerLike, QuestionLike
from .forms import LoginForm, RegistrationForm, SettingsForm, AskForm, AnswerForm


def paginate(objects_list, request, per_page=20):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(objects_list, per_page)
    page = paginator.page(page_num)
    return page


def authentificate(request, form):
    user = auth.authenticate(request, **form.cleaned_data)
    if user:
        auth.login(request, user)
        next = request.POST.get('next')
        if next and next != '/login/':
            return redirect(next)
        return redirect(reverse('index'))
    elif Profile.objects.exist(login=form.cleaned_data.get('username')):
        form.add_error('password', 'Password is incorrect')
    else:
        form.add_error('username', 'User does not exist')
    return None


def registrate(request, form):
    user = form.create_user()
    auth.login(request, user)
    return redirect(reverse('index'))


def index(request):
    page = paginate(Question.objects.all(), request)
    return render(request, 'index.html', context={
        'questions': page.object_list,
        'page_obj': page
    })


def question(request, question_id):
    question = Question.objects.get(question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST, user=request.user, question=question)
        if form.is_valid():
            form.create_answer()
            return redirect(reverse('question', kwargs={'question_id': question_id}))
    else:
        form = AnswerForm(user=request.user)
    
    page = paginate(Answer.objects.get_by_question(question_id), request, 30)
    return render(request, 'question.html', context={
        'question': question,
        'answers': page.object_list,
        'page_obj': page,
        'form': form
    })


def hot(request):
    page = paginate(Question.objects.get_hot(), request)
    return render(request, 'hot.html', context={
        'questions': page.object_list,
        'page_obj': page
    })


def tag(request, tag_id):
    page = paginate(Question.objects.get_by_tag(tag_id), request)
    return render(request, 'tag.html', context={
        'tag': Tag.objects.get(tag_id),
        'questions': page.object_list,
        'page_obj': page
    })


def user(request, user_id):
    page = paginate(Question.objects.get_by_user(user_id), request)
    return render(request, 'user.html', context={
        'user': User.objects.get(pk=user_id),
        'questions': page.object_list,
        'page_obj': page
    })


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            response = authentificate(request, form)
            if response:
                return response
    else:
        form = LoginForm()
    return render(request, 'login.html', context={'form': form})


def logout(request):
    auth.logout(request)
    next = request.GET.get('next', 'index')
    return redirect(next)


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            response = registrate(request, form)
            if response:
                return response
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', context={'form': form})


@login_required
def settings(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.update_user()
    else:
        form = SettingsForm(user=request.user)
    return render(request, 'settings.html', context={'form': form})


@login_required
def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST, user=request.user)
        if form.is_valid():
            return redirect(reverse('question', kwargs={'question_id': form.create_question()}))
    else:
        form = AskForm(user=request.user)
    return render(request, 'ask.html', context={'form': form})


def pageNotFound(request, exception):
    return render(request, 'error.html', context={'error': '404'})


def serverError(request):
    return render(request, 'error.html', context={'error': '500'})