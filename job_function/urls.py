"""
URL configuration for Job_Portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from job_function.views import list_applicants, list_post_jobs, post_job

urlpatterns = [
    path('post_job/', post_job),
    path('list_posted_jobs/', list_post_jobs),
    path('list_applicants/<str:job_id>/', list_applicants),
]
