"""
URL configuration for bracketcreator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from bracket_creator import views as bracket_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', bracket_views.signup_view, name='signup'),

    path('', bracket_views.BracketListView.as_view(), name='bracket-list'),
    path('create/', bracket_views.BracketCreateView.as_view(), name='bracket-create'),
    path('bracket/<int:pk>/', bracket_views.BracketDetailView.as_view(), name='bracket-detail'),
    path('bracket/<int:pk>/delete/', bracket_views.BracketDeleteView.as_view(), name='bracket-delete'),
    path('bracket/<int:bracket_pk>/participants/', bracket_views.ParticipantCreateView.as_view(), name='participant-add'),
    path('bracket/<int:bracket_pk>/participants/update/', bracket_views.BracketUpdateView.as_view(), name='participant-update'),
]
