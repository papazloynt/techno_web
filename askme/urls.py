"""askme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
#    path('admin/', admin.site.urls),
    path('', views.login, name="login"),
    path('new_question/', views.new_question, name="new_question"),
    path('question/', views.question, name="question"),
    path('questions/', views.questions, name="questions"),
    path('registr/', views.reg, name="reg"),
    path('settings/', views.settings, name="settings"),
    path('tag/', views.tag, name="tag"),
    path('wrong_new_question/', views.wrong_new_question, name="wrong_new_question"),
]
