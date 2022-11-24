from atexit import register
from django.shortcuts import render, redirect, get_object_or_404

from django.http import Http404
from django.http import JsonResponse
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
import json
import base64

# Create your views here.


def authorize_by_request(request):
    authorization_header = request.META['HTTP_AUTHORIZATION']
    base64_bytes = authorization_header.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    credentials = message.split(' ')
    user = authenticate(request,username=credentials[0],password=credentials[1])
    if user is not None:
        login(request, user)
        return user
    else:
        return HttpResponse(status=401)

def get_courses(request):
    courses = list(Course.objects.values())
    return JsonResponse(courses, safe = False)

def get_users(request):
    role = request.GET.get('role')
    print('Role is'+ role)
    if role != None:
        users = list(Person.objects.filter(role=role).values())
    else:
        users = list(Person.objects.values())
    return JsonResponse(users, safe = False)

def get_course_by_id(request, id):
    course = Course.objects.filter(id_course=id).values()[0]
    return JsonResponse(course, safe = False)

def get_logged_user(request):
    user = authorize_by_request(request=request)
    person_instance = list(Person.objects.filter(user=request.user).values())[0]
    return JsonResponse(person_instance, safe = False)


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)

            username = json_data['username']
            firstName = json_data['firstName']
            lastName = json_data['lastName']
            email = json_data['email']
            password = json_data['password']

            user_instance = User.objects.create_user(username=username, email=email, password=password)
            user = Person.objects.create(user=user_instance, firstname=firstName, surname=lastName, email=email, role='s')

            if user is not None:
                return HttpResponse('ok')
            else:
                return HttpResponse(status=500)
        except:
            return HttpResponse(status=500)


def profile_edit(request, id):
    if request.method == 'POST':
        try:
            person_instance = Person.objects.filter(id_person=id).first()
            json_data = json.loads(request.body)

            firstname = json_data.get('firstname') if json_data.get('firstname') != None else person_instance.firstname
            surname = json_data.get('surname') if json_data.get('surname') != None else person_instance.surname
            address = json_data.get('address') if json_data.get('address') != None else person_instance.address
            email = json_data.get('email') if json_data.get('email') != None else person_instance.email
            telephone = json_data.get('telephone') if json_data.get('telephone') != None else person_instance.telephone
            role = json_data.get('role') if json_data.get('role') != None else person_instance.role

            active_person = Person.objects.filter(user=request.user).first()
            if role != None and active_person.is_admin == False:
                return HttpResponse(status=500)
            elif active_person.is_admin == False and person_instance.id_person != active_person.id_person:
                return HttpResponse(status=500)

            Person.objects.filter(id_person=person_instance.id_person).update(firstname=firstname,
                                                                              surname=surname,
                                                                              address=address,
                                                                              telephone=telephone,
                                                                              email=email,role=role)
            return HttpResponse('ok')
        except:
            return HttpResponse(status=500)


def course_edit(request, id):
    if request.method == 'POST':
        try:
            person_instance = Person.objects.filter(user=request.user).first()
            if person_instance.is_garant == False:
                return HttpResponse(status=500)

            course_instance = Course.objects.filter(id_course=id).first()
            json_data = json.loads(request.body)

            abbrv = json_data.get('abbrv') if json_data.get('abbrv') != None else course_instance.abbrv
            title = json_data.get('title') if json_data.get('title') != None else course_instance.title
            description = json_data.get('description') if json_data.get('description') != None else course_instance.description
            credits = json_data.get('credits') if json_data.get('credits') != None else course_instance.credits
            max_persons = json_data.get('max_persons') if json_data.get('max_persons') != None else course_instance.max_persons
            approved = json_data.get('approved') if json_data.get('approved') != None else course_instance.approved
            type = json_data.get('type') if json_data.get('type') != None else course_instance.type


            Course.objects.filter(id_course=course_instance.id_course).update(abbrv=abbrv,
                                                                              title=title,
                                                                              description=description,
                                                                              max_persons=max_persons,
                                                                              credits=credits,
                                                                              approved=approved, 
                                                                              type=type)
            return HttpResponse('ok')
        except:
            return HttpResponse(status=500)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            username = json_data['username']
            password = json_data['password']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request, user)
                print(request.user)
                return HttpResponse('ok')
            else:
                return HttpResponse(status=401)
        except:
            return HttpResponse(status=500)

def index(request):
    course = Course.objects.all()

    person_instance = None
    if request.user.is_authenticated:
        person_instance = Person.objects.filter(user=request.user).first()
    context = {
            'course' : course,
            "person": person_instance
        }
    return render(request, 'index.html', context)

def page404(request, exception):
    return render(request, '404.html', status=404)


def access_failed(request):

    person_instance = None
    if request.user.is_authenticated:
        person_instance = Person.objects.filter(user=request.user).first()
    context = {
            "person": person_instance
        }
    return render(request, 'access_denied.html', context)




def logout_user(request):
    logout(request)
    messages.success(request,"You Were logout")
    return redirect("/")


def logged_view(request):
    context = {
    }

    return render(request, 'logged_on.html', context)


def courses_view(request, id):
    course = Course.objects.filter(id_course=id).first()
    is_register = False
    if request.user.is_authenticated:
        person_instance = Person.objects.filter(user=request.user).first()
        courses_user = person_instance.courses.all()

        for i in courses_user:
            if i.abbrv == course.abbrv:
                is_register = True
                break


        if request.method == "POST":

            if 'Register' in request.POST:
                person_instance.courses.add(course)   
                person_instance.save() 
                is_register = True

            elif 'Unregister' in request.POST:
                person_instance.courses.remove(course)
                person_instance.save()
                is_register = False

    context = {
        "course" : course,
        "course_abbrv" : course.abbrv,
        "course_title" : course.title,
        "is_register" : is_register,
        #'person' : person_instance,
    }

    return render(request, 'course_detail.html', context)

@login_required
def study_view(request):
    if request.user.is_authenticated:
        person_instance = Person.objects.filter(user=request.user).first()
        courses = person_instance.courses.all()

    contex = {
        'courses' : courses,
    }
    return render(request, 'study_view.html',contex)





@login_required
def admin_view(request):
    if request.user.is_authenticated:
        person_instance = Person.objects.filter(user=request.user).first()

        if person_instance.role != 'a':
            redirect("/access_failed")
            raise Http404

        persons = Person.objects.all()
        context = {
            "person": person_instance,
            "persons" : persons
        }
    else:
        raise Http404

    return render(request, 'admin_view.html', context)
@login_required
def study_view(request):
    if request.user.is_authenticated:
        person_instance = Person.objects.filter(user=request.user).first()
        courses = person_instance.courses.all()

    contex = {
        'courses' : courses,
    }
    
    return render(request, 'study_view.html',contex)


@login_required
def profile_view(request):
    if request.user.is_authenticated:
        person_instance = Person.objects.filter(user=request.user).first()
        
        context = {
            "person": person_instance,
            "role" : person_instance.role
        }
    else:
        raise Http404

    return render(request, 'profile.html', context)


def user_delete(request, id):
    person_instance = Person.objects.filter(id_person=id).first()
    if request.method == 'POST':
        if 'Delete' in request.POST:
            Person.objects.get(id_person=person_instance.id_person).delete()
            User.objects.filter(username=person_instance.user).delete()
        return redirect('/admin_view')
    context = {
        'person': person_instance,
    }
    return render(request, 'admin_user_delete.html', context)
    

def user_update(request, id):
    person_instance = Person.objects.filter(id_person=id).first()
    if request.method == 'POST':
        person_instance = Person.objects.filter(id_person=id).first()

        form = UpdateUser(request.POST or None)
        if form.is_valid():
            role = form.cleaned_data['role'] if form.cleaned_data['role'] != '' else person_instance.role
            Person.objects.filter(id_person=person_instance.id_person).update(role=role)
            person_instance = Person.objects.filter(id_person=id).first()
            return redirect('/admin_view')
    else:
        form = UpdateUser()    

    context = {
        'form' : form,
        'person': person_instance,
    }
    return render(request, 'admin_user_update.html', context)




@login_required
def garant_view(request):
    if request.user.is_authenticated:
        person_instance = Person.objects.filter(user=request.user).first()
        courses = person_instance.courses.all()
        if person_instance.role != 'g':
            return redirect('/access_failed')
            raise Http404

        context = {
            "person": person_instance,
            'courses' : courses
        }
    else:
        raise Http404

    return render(request, 'garant_view.html', context)


@login_required
def students_view(request, id):
    if request.user.is_authenticated:
        person_instance = Person.objects.filter(user=request.user).first()
        if person_instance.role != 'g':
            return redirect('/access_failed')
            raise Http404
        course = Course.objects.filter(id_course=id).first()
        students = Person.objects.filter(courses=course).all()
    else:
        raise Http404
    context = {
            "person": person_instance,
            'courses' : course,
            'students' : students
        }

    return render(request, 'list_of_students.html', context)



def create_course(request):
    if request.method == 'POST':
        try:
            active_person = Person.objects.filter(user=request.user).first()
            if active_person.is_garant == False:
                return HttpResponse(status=500)

            json_data = json.loads(request.body)

            abbrv = json_data['abbrv']  
            title = json_data['title']  
            description = json_data['description']  
            credits = json_data['credits']  
            max_persons = json_data['max_persons']  
            garant = json_data['username'] 

            user_instance = User.objects.filter(username=garant).first()
            person_instance = Person.objects.filter(user=user_instance).first()

            try:
                Course.objects.create(abbrv=abbrv,title=title,description=description,
                                        credits=credits,max_persons=max_persons,
                                        garant_id=person_instance,approved=0)
            except:
                print("error create course")    

            return HttpResponse('ok')

        except:
            return HttpResponse(status=500)


#@login_required
def get_course_user(request,id):
    if request.user.is_authenticated:
        student_course = list(Student_Course.objects.filter(id_student = id).values())
        course_list = list()
        for item in student_course:
            course = Course.objects.filter(id_course = item['id_course_id']).values()[0]
            course_list.append(course)
        return JsonResponse(course_list, safe = False)
    else:
       return HttpResponse(status=500)


def add_user_to_course(request, id_person, id_course):
    if request.method == 'POST':
        course = Course.objects.filter(id_course=id_course).first()
        person = Person.objects.filter(id_person=id_person).first()
        Student_Course.objects.create(id_student=person, id_course=course)
        return HttpResponse('ok')

def remote_user_from_course(request, id_person, id_course):
    if request.method == 'POST':
        course = Course.objects.filter(id_course=id_course).first()
        person = Person.objects.filter(id_person=id_person).first()
        Student_Course.objects.filter(id_student=person,id_course=course).delete()
        return HttpResponse('ok')