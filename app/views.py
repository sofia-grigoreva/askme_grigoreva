from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import Tag, Profile, Question, Answer, AnswerLike, QuestionLike
from django.contrib.auth.models import User

def paginate(objects_list, request, per_page=20):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(objects_list, per_page)
    page = paginator.page(page_num)
    return page

def index(request):
    page = paginate(Question.objects.all(), request)
    return render(request, 'index.html', context={'questions' : page.object_list, 'page_obj' : page})

def question(request, question_id):
    page = paginate(Answer.objects.get_by_question(question_id), request, 30)
    return render(request, 'question.html', context={'question' : Question.objects.get(question_id), 'answers' : page.object_list, 'page_obj' : page})

def hot(request):
    page = paginate(Question.objects.get_hot(), request)
    return render(request, 'hot.html', context={'questions' : page.object_list, 'page_obj' : page})

def tag(request, tag_id):
    page = paginate(Question.objects.get_by_tag(tag_id), request)
    return render(request, 'tag.html', context={'tag' : Tag.objects.get(tag_id), 'questions' : page.object_list, 'page_obj' : page})

def user(request, user_id):
    page = paginate(Question.objects.get_by_user(user_id), request)
    return render(request, 'user.html', context={'user' : User.objects.get(pk=user_id), 'questions' : page.object_list, 'page_obj' : page})

def ask(request):
    return render(request, 'ask.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def signup(request):
    return render(request, 'signup.html')

def settings(request):
    return render(request, 'settings.html')

def pageNotFound(request, exception):
    return render(request, 'error.html', context={'error' : '404'})

def serverError(request):
    return render(request, 'error.html', context={'error' : '500'})
