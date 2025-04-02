from django.shortcuts import render
from django.core.paginator import Paginator

QUESTIONS = [
    {
        'title': f'Title {i}',
        'id': i ,
        'text': "The question is about ..................",
        'ansnumber' : i,
        'answers' : [1]*30,
        'tags' : [1,2,3]
    } for i in range(50)
]

POPULARTAGS = [
    {
        'id': i ,
        'questions' : [1]*30

    } for i in range(10)
]

def paginate(objects_list, request, per_page=10):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(objects_list, per_page)
    page = paginator.page(page_num)
    return page

def index(request):
    page = paginate(QUESTIONS, request)
    return render(request, 'index.html', context={'questions' : page.object_list, 'page_obj' : page, 'popular_tags' : POPULARTAGS})

def hot(request):
    page = paginate(QUESTIONS, request)
    return render(request, 'hot.html', context={'questions' : page.object_list, 'page_obj' : page, 'popular_tags' : POPULARTAGS})

def question(request, question_id):
    page = paginate(QUESTIONS[question_id]['answers'], request)
    return render(request, 'question.html', context={'question' : QUESTIONS[question_id], 'answers' : page.object_list, 'page_obj' : page, 'popular_tags' : POPULARTAGS})

def ask(request):
    return render(request, 'ask.html', context={'popular_tags' : POPULARTAGS})

def login(request):
    return render(request, 'login.html', context={'popular_tags' : POPULARTAGS})

def signup(request):
    return render(request, 'signup.html', context={'popular_tags' : POPULARTAGS})

def signup(request):
    return render(request, 'signup.html', context={'popular_tags' : POPULARTAGS})

def settings(request):
    return render(request, 'settings.html', context={'questions' : QUESTIONS, 'popular_tags' : POPULARTAGS})

def tag(request, tag_id):
    page = paginate(QUESTIONS, request)
    return render(request, 'tag.html', context={'tag' : tag_id, 'questions' : page.object_list, 'page_obj' : page, 'popular_tags' : POPULARTAGS})