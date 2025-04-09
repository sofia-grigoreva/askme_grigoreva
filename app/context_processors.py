
from django.shortcuts import render
from app.models import Tag, Profile

def popular_tags():
    return Tag.objects.get_top()

def popular_users():
    return Profile.objects.get_top()

def popular(request):
    return {'popular_tags' : popular_tags, 'popular_users': popular_users}