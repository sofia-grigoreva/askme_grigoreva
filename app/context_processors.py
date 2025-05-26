
from django.shortcuts import render
from django.core.cache import cache

def popular(request):
    return {'popular_tags' : cache.get("popular_tags"), 'popular_users': cache.get("popular_users")}