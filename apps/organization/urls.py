# encoding: utf-8
__author__ = 'mark'
__date__ = '2018/3/14 10:41'

from django.urls import path,include,re_path
from organization.views import OrgView,AddUserAskView,OrgHomeView,OrgCourseView,OrgDescView,OrgTeacherView,AddFavView
from organization.views import TeacherListView,TeacherDetailView

app_name = "organization"

urlpatterns = [
    #机构
    path('list/', OrgView.as_view(), name="org_list"),
    path('add_ask/',AddUserAskView.as_view(),name='add_ask'),
    re_path('home/(?P<org_id>\d+)/', OrgHomeView.as_view(), name='org_home'),
    re_path('course/(?P<org_id>\d+)/', OrgCourseView.as_view(), name='org_course'),
    re_path('desc/(?P<org_id>\d+)/', OrgDescView.as_view(), name='org_desc'),
    re_path('org_teacher/(?P<org_id>\d+)/', OrgTeacherView.as_view(), name='org_teacher'),

    #机构收藏
    path('add_fav/', AddFavView.as_view(), name="add_fav"),

    #讲师列表页
    path('teacher/list/', TeacherListView.as_view(), name="teacher_list"),

    # 讲师详情页
    re_path('teacher/detail/(?P<teacher_id>\d+)/', TeacherDetailView.as_view(), name="teacher_detail"),

]