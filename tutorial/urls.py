# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from django.urls import path

from . import views

urlpatterns = [
  # /
  path('', views.home, name='home'),
  # TEMPORARY
  path('signin', views.sign_in, name='signin'),
  path('signout', views.sign_out, name='signout'),
  path('callback', views.callback, name='callback'),
  path('calendar', views.calendar, name='calendar'),
  path('sharedfiles', views.sharedfiles, name='sharedfiles'),
  path('register', views.registerPage, name='register'),
  path('login', views.loginPage, name='login'),
  path('logout', views.logoutUser, name='logout'),
  path('files', views.files, name='files'),
  path('upload', views.upload_file, name='upload'),
  path('createacademiccourse', views.create_course, name='createacademiccourse'),
  path('moveusertoread/<str:file_id>/<str:file_name>', views.move_user_to_read, name='moveusertoread'),
  path('uploadadmin/<str:file_id>/<str:file_name>', views.upload_file_admin, name='uploadadmin'),
]
