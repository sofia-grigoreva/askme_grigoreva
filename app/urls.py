from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('hot/', views.hot, name="hot"),
    path('ask/', views.ask, name="ask"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('question/<int:question_id>/', views.question, name="question"),
    path('tag/<int:tag_id>/', views.tag, name="tag"),
    path('settings/', views.settings, name="settings"),
]