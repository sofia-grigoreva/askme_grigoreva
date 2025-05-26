from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.contrib import auth
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from .models import Tag, Profile, Question, Answer, AnswerLike, QuestionLike
from .forms import LoginForm, RegistrationForm, SettingsForm, AskForm, AnswerForm
from django.contrib import messages
from django.conf import settings
import jwt
import time
import json
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


def paginate(objects_list, request, per_page=20):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(objects_list, per_page)
    page = paginator.page(page_num)
    return page


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
            data = form.save()
            return redirect(reverse('question', kwargs={'question_id': question_id}))
    else:
        form = AnswerForm(user=request.user)
    
    page = paginate(Answer.objects.get_by_question(question_id), request, 30)
    token = jwt.encode({"sub": str(request.user.id), "exp": int(time.time()) + 10*60}, settings.CENTRIFUGO_HMAC_SECRET, algorithm="HS256")
    return render(request, 'question.html', context={
        'question': question,
        'answers': page.object_list,
        'page_obj': page,
        'form': form,
        'token': token,
        "cfurl": settings.CENTRIFUGO_URL
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
            user = auth.authenticate(request, **form.cleaned_data)
            auth.login(request, user)
            next = request.POST.get('next')
            if next and next != '/login/':
                return redirect(next)
            return redirect(reverse('index'))
    else:
        form = LoginForm()
    return render(request, 'login.html', context={'form': form})


def logout(request):
    auth.logout(request)
    next = request.GET.get('next', 'index')
    return redirect(next)


def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect(reverse('index'))
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', context={'form': form})


@login_required
def edit(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect(reverse('settings'))
    else:
        form = SettingsForm(user=request.user)
    return render(request, 'settings.html', context={'form': form})


@login_required
def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST, user=request.user)
        if form.is_valid():
            return redirect(reverse('question', kwargs={'question_id': form.save()}))
    else:
        form = AskForm(user=request.user)
    return render(request, 'ask.html', context={'form': form})


def updatelikes(object, type, id, user):
    status = "None"
    obj = object.objects.get(id)
    if type == "like":
        type = True
    else:
        type = False
    like = obj.get_like(user)
    if like:
        if like.type == type:
            like.delete()
        else:
            like.type = type
            like.save()
            status = type
    else:
        obj.create_like(user=user, type=type)
        status = type
    score = obj.get_likes()
    return JsonResponse({"score": f'{score}', "status" : f'{status}'})


@login_required
@require_POST
def like(request, id):
    if request.method == 'POST':
        type = json.loads(request.body).get('type')
        object = json.loads(request.body).get('object')
    if object == "question":
        return updatelikes(Question, type, id, request.user)
    return updatelikes(Answer, type, id, request.user)


@login_required
@require_POST
def check(request, id):
    if request.method == 'POST':
        answer = Answer.objects.get(id)
        answer.is_checked = not(answer.is_checked)
        answer.save()
    return JsonResponse({"status" : f'{answer.is_checked}'})


@require_GET
def suggestions(request):
    query = request.GET.get('q', '').strip()
    questions = Question.objects.annotate(q=SearchVector('title') + SearchVector('text')).filter(q=query)[:10]
    suggestions = [
        {
            'id': q.id,
            'title': q.title,
            'text': q.text
        }
        for q in questions
    ]
    return JsonResponse({'results': suggestions})


@require_GET
def search(request):
    query = request.GET.get('q', '').strip()
    questions = Question.objects.annotate(q=SearchVector('title') + SearchVector('text')).filter(q=query)
    page = paginate(questions, request)
    if len(questions) == 0:
        return render(request, 'search.html', context={
        'title': "Nothing found for your request",
    })
    page = paginate(questions, request)
    title = "Explore Results for: " + query
    return render(request, 'search.html', context={
        'questions': page.object_list,
        'page_obj': page,
        'title': title,
    })


def pageNotFound(request, exception):
    return render(request, 'error.html', context={'error': '404'})


def serverError(request):
    return render(request, 'error.html', context={'error': '500'})