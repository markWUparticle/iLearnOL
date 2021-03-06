from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse  #指名返回的数据类型
from django.db.models import Q

from .models import CourseOrg,CityDict,Teacher
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite

# Create your views here.

class OrgView(View):
    '''
    课程机构列表
    '''
    def get(self,request):
        all_orgs = CourseOrg.objects.all().order_by('-fav_nums')    
        all_citys = CityDict.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')[:3]  #排名前三的热门机构提取

        # 机构搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                address__icontains=search_keywords)) # 前缀i代表不区分大小写

        #取出筛选城市
        city_id = request.GET.get('city','')
        if city_id:
            all_orgs = all_orgs.filter(city_id =int(city_id))

        #类别筛选
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)
        org_nums = all_orgs.count()  # 放在筛选后统计机构数量

        #排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        #课程机构进行分页
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs,4,request=request)  #每页取5个显示
        orgs = p.page(page)


        return render(request,'org-list.html',{
            'all_orgs':orgs,
            'all_citys':all_citys,
            'org_nums': org_nums,
            'city_id':city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sort,
            'search_keywords':search_keywords
        })


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"您的字段有错误,请检查"}', content_type='application/json')


class OrgHomeView(View):
    '''
    机构首页
    '''
    def get(self,request,org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums +=1
        course_org.save()
        #查询用户是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all().order_by('-click_nums')[:4]  #外键 取出所有课程
        teachers = course_org.teacher_set.all().order_by('-click_nums')[:1]
        courses = course_org.course_set.filter(teacher=teachers)[:1]

        return render(request,'org-detail-homepage.html',{
            'courses':courses,
            'all_courses':all_courses,
            'teachers':teachers,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav,
        })


class OrgCourseView(View):
    '''
    机构课程列表页
    '''
    def get(self,request,org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all().order_by('-click_nums')  #外键 取出所有课程

        # 查询用户是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request,'org-detail-course.html',{
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav': has_fav,
        })


class OrgDescView(View):
    '''
    机构介绍页
    '''
    def get(self,request,org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 查询用户是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request,'org-detail-desc.html',{
            'course_org':course_org,
            'current_page':current_page,
            'has_fav': has_fav,
        })

class OrgTeacherView(View):
    '''
    机构讲师介绍
    '''
    def get(self,request,org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()

        # 查询用户是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request,'org-detail-teachers.html',{
            'course_org':course_org,
            'all_teachers':all_teachers,
            'current_page':current_page,
            'has_fav': has_fav,
        })



class AddFavView(View):
    '''
    用户收藏及取消功能
    '''
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)  #没有就返回0  返回空会报异常
        fav_type = request.POST.get('fav_type',0)
        #判断用户是否用户
        if not request.user.is_authenticated:  #判断用户是否登录
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))  #联合查询  module里面要求了Int类型 要转换
        if exist_records:
            #如果记录存在，则表示用户取消收藏
            exist_records.delete()

            #取消收藏 收藏数-1
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -=1
                if course.fav_nums <0 :
                    course.fav_nums = 0
                course.save()

            if int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -=1
                if course_org < 0:
                    course_org = 0
                course_org.save()

            if int(fav_type) == 3 :
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -=1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status":"fail", "msg":"已取消收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) >0 and int(fav_type)>0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type=int(fav_type)
                user_fav.save()

                # 收藏数+1
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()

                if int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()

                if int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')



class TeacherListView(View):
    '''
    讲师列表页
    '''
    def get(self,request):
        all_teachers =Teacher.objects.all().order_by('-fav_nums')    
        teacher_nums = all_teachers.count()

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords) | Q(work_company__icontains=search_keywords)| Q(work_postion__icontains=search_keywords))
	
        # 排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_nums')

        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]  #讲师排行

        #课程讲师分页
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 4, request=request)  # 每页取5个显示
        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'all_teachers': teachers,
            "teacher_nums": teacher_nums,
            'sorted_teacher':sorted_teacher,
            'sort':sort,
            'teacher_nums':teacher_nums,
            'search_keywords':search_keywords,
         })

class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id = int(teacher_id))
        all_courses = teacher.course_set.all()
        teacher.click_nums +=1
        teacher.save()
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]

        #收藏显示
        has_teacher_faved = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
                has_teacher_faved = True

        has_org_faved = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
                has_org_faved = True

        return render(request, "teacher-detail.html", {
            'teacher':teacher,
            'all_courses':all_courses,
            'sorted_teacher':sorted_teacher,
            'has_org_faved':has_org_faved,
            'has_teacher_faved':has_teacher_faved,

        })


