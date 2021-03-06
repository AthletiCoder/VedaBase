"""VedaBase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from verses.api.verse import VerseHandler, next_verse, prev_verse, AdditionalDetails
from verses.api.tag import TagTranslationHandler, TagPurportSectionHandler, get_tags
from accounts.auth import login, logout, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('verse/', VerseHandler.as_view()),
    path('verse/tagTranslation', TagTranslationHandler.as_view()),
    path('verse/tagTranslation/<int:id>/', TagTranslationHandler.as_view()),
    path('verse/tagPurportSection', TagPurportSectionHandler.as_view()),
    path('verse/tagPurportSection/<int:id>/', TagPurportSectionHandler.as_view()),
    path('verse/additional-details', AdditionalDetails.as_view()),
    path('login/', login),
    path('logout/', logout),
    path('register/', register),
    path('next-verse/', next_verse),
    path('prev-verse/', prev_verse),
    path('get-tags/', get_tags),
]
