from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('hot/', views.hot, name="hot"),
    path('ask/', views.ask, name="ask"),
    path('login/', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('signup/', views.signup, name="signup"),
    path('question/<int:question_id>/', views.question, name="question"),
    path('tag/<int:tag_id>/', views.tag, name="tag"),
    path('profile/edit/', views.settings, name="settings"),
    path('user/<int:user_id>/', views.user, name="user"),
    path('like/<int:id>/', views.like, name="like"),
    path('check/<int:id>/', views.check, name="check"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)