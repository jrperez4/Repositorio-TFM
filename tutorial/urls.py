# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from django.urls import path, re_path

from . import views
from .views import CategoryListView

urlpatterns = [
  # /
  path('', views.home, name='home'),
  # TEMPORARY
  path('home', views.home, name='home'),
  path('signin', views.sign_in, name='signin'),
  path('signout', views.sign_out, name='signout'),
  path('callback', views.callback, name='callback'),
  path('calendar', views.calendar, name='calendar'),
  path('sharedfiles', views.render_pdf_view, name='sharedfiles'),
  path('register', views.registerPage, name='register'),
  path('downloadreceipt', views.render_pdf_view, name='downloadreceipt'),
  path('login', views.loginPage, name='login'),
  path('logout', views.logoutUser, name='logout'),
  path('files', views.files, name='files'),
  path('files/<str:file_name>', views.files, name='files'),
  path('files/moveusertoread/<str:file_id>/<str:file_name>', views.move_user_to_read, name='files'),
  path('files/moveusertoread/<str:file_id>/<str:file_name>/<str:course>', views.move_user_to_read, name='files'),
  path('files/uploadadmin/<str:file_id>/<str:file_name>/<str:course>', views.upload_file_admin, name='files'),
  path('files/uploadadminrecord/<str:file_id>/<str:file_name>/<str:course>', views.upload_record_file_admin, name='files'),
  path('files/changetutors/<str:file_name>/<str:id_file>', views.change_tutors, name='changetutors'),
  path('files/changetutors/<str:file_name>/<str:id_file>/<str:course>', views.change_tutors, name='changetutors'),
  path('filesreaded', views.files_readed, name='filesreaded'),
  path('filesreaded/<str:course>', views.files_readed, name='filesreaded'),
  path('upload', views.upload_file, name='upload'),
  path('createacademiccourse', views.create_course, name='createacademiccourse'),
  path('moveusertoread/<str:file_id>/<str:file_name>', views.move_user_to_read, name='moveusertoread'),
  path('moveusertoread/<str:file_id>/<str:file_name>/<str:course>', views.move_user_to_read, name='moveusertoread'),
  path('uploadadmin/<str:file_id>/<str:file_name>', views.upload_file_admin, name='uploadadmin'),
  path('uploadadminrecord/<str:file_id>/<str:file_name>', views.upload_record_file_admin, name='uploadadminrecord'),
  path('uploadadminrecord/<str:file_id>/<str:file_name>/<str:course>', views.upload_record_file_admin, name='uploadadminrecord'),
  path('createstudentfile', views.create_student_file, name='createstudentfile'),
  path('searchfiles', views.bibliography, name='searchfiles'),
  path('detailedfile', views.detailed_file, name='detailedfile'),
  path('detailedfile/<str:dni>/',views.detailed_file, name='detailedfile'),
  path('showpdf/<str:memoir>', views.show_pdf, name='showpdf'),
  path('changetutors/<str:file_name>/<str:id_file>', views.change_tutors, name='changetutors'),
  path('changetutors/<str:file_name>/<str:id_file>/<str:course>', views.change_tutors, name='changetutors'),
  path('category/list/', CategoryListView.as_view(), name='category_list'),



]
