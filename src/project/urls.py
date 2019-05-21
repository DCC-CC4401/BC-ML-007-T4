"""project URL Configuration

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

from users.views import landing_page, evaluators_page
from courses.views import courses_page
from evaluations.views import evaluations_page

urlpatterns = [
    path('', landing_page, name="Landing Page"),
    path('cursos/', courses_page, name="Courses Page"),
    path('evaluadores/', evaluators_page, name="Evaluators Page"),
    path('evaluaciones/', evaluations_page, name="Evaluations Page"),
    path('admin/', admin.site.urls),
]
